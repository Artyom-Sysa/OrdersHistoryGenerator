import datetime
import logging
import os
import re

from Config.ConfigLoader.ConfigLoaderImplementation.IniFileConfigLoader import IniFileConfigLoader
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Generators.PseudorandomNumberGeneratorImplementation.IdGenerator import IdGenerator
from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import LoggingLevel as Level
from Utils.Utils import Utils


class Launcher:
    def start(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Launcher started')
        self.__load_configs()
        self.__configurate_logger()
        self.__execute_prepare_configurations_for_generation()

    def __load_configs(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Started load configuration')

        self.configs = Configuration()
        self.config_loader = IniFileConfigLoader()
        self.config_loader.load(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.DEFAULT_SETTING_FILE_PATH])

        Logger.add_to_journal(__file__, Level.INFO, 'Loading configuration finished')
        Logger.add_to_journal(__file__, Level.DEBUG, 'Loaded configurations :\n{}'.format(self.configs.settings))

    def __configurate_logger(self):
        '''
        Configuration python in-build logger with config object parameters
        '''

        Logger.add_to_journal(__file__, Level.INFO, 'Start execution function of configuration logger')

        logging.basicConfig(
            filename=os.path.join(self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH],
                                  Utils.get_current_date_with_format() + ".log"),
            filemode='a',
            format=self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%%', '%'),
            datefmt=self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%%', '%'),
            level=self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])

        Logger.add_to_journal(__file__, Level.INFO, 'Execution function of configuration logger finished')
        Logger.debug(__file__,
                     'Logger configurated with values: filename: {} | filemode: {} | format: {} | datefmt: {} | level: {}'.format(
                         os.path.join(self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH],
                                      Utils.get_current_date_with_format() + ".log"),
                         'a',
                         self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%', '%%'),
                         self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%',
                                                                                                              '%%'),
                         self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])
                     )

        Utils.create_folder_if_not_exists(self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH])

    def __load_currency_pairs_from_file(self):
        '''
        Load currency pairs from file by path in config object
        '''

        Logger.info(__file__, 'Start loading currency pairs from file {}'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

        try:
            with open(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH], "r") as file:
                for line in file.readlines():
                    if re.fullmatch(r'[a-zA-Z]{3}\/[a-zA-Z]{3};[0-9]+([\.|\,][0-9]{0,5})', line.replace('\n', '')):
                        parts = line.split(";")
                        self.configs.currency_pairs.append({
                            Values.CURRENCY_PAIR_NAME: parts[0],
                            Values.CURRENCY_PAIR_VALUE: float(parts[1].replace("\n", '').replace(',', '.'))
                        })

                self.configs.settings[Values.CURRENCY_PAIR_GENERATOR][LCGParams.MODULUS.value] = len(
                    self.configs.currency_pairs)

            Logger.info(__file__, 'Loading currency pairs from file {} finished'.format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

            Logger.debug(__file__, 'Loaded {} currency pairs: {}'.format(len(self.configs.currency_pairs),
                                                                         self.configs.currency_pairs))
        except:
            Logger.error(__file__, "Loading currency pairs from file {} failed".format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

    def __load_tags_from_file(self):
        '''
        Load tags from file by path in config object
        '''

        Logger.info(__file__, 'Start loading tags from file {}'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

        try:
            with open(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH], "r") as file:
                for line in file.readlines():
                    if re.fullmatch('[a-zA-Z]{0,10}', line.replace('\n', '')):
                        self.configs.tags.append(line.replace("\n", ''))

            Logger.info(__file__, 'Loading tags from file {} finished'.format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

            Logger.debug(__file__, 'Loaded {} tags: {}'.format(len(self.configs.tags), ', '.join(self.configs.tags)))

            self.configs.settings[Values.TAGS_GENERATOR_1][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_2][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_3][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_4][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
            self.configs.settings[Values.TAGS_GENERATOR_5][LCGParams.MODULUS.value] = int(len(self.configs.tags) * 1.5)
        except:
            Logger.error(__file__, "Loading tags from file {} failed".format(
                self.configs.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

    def __calculate_orders_period_volumes(self):
        '''
        Calculate orders volumes list than equal to percentage of zones:
        red = 15%, green = 60% and blue = 25%
        '''

        red_zone_percent = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.RED_ZONE_ORDERS_PERCENT]
        green_zone_percent = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.GREEN_ZONE_ORDERS_PERCENT]
        blue_zone_percent = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BLUE_ZONE_ORDERS_PERCENT]

        Logger.info(__file__,
                    'Started calculating of orders volumes to period with zones percentes: red = {}, green ={}, blue ={}'.format(
                        red_zone_percent, green_zone_percent, blue_zone_percent
                    ))

        for i in range(1, self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT] + 1):
            first_percent = Utils.calculate_percent_from_value(i, red_zone_percent)
            second_percent = Utils.calculate_percent_from_value(i, green_zone_percent)
            third_percent = Utils.calculate_percent_from_value(i, blue_zone_percent)

            if Utils.is_int(first_percent) and Utils.is_int(second_percent) and Utils.is_int(third_percent):
                self.configs.orders_volumes.append({
                    Values.TOTAL_ORDERS_VOLUME: i,
                    Values.RED_ZONE_VOLUME: first_percent,
                    Values.GREEN_ZONE_VOLUME: second_percent,
                    Values.BLUE_ZONE_VOLUME: third_percent
                })

        Logger.info(__file__, 'Calculating of orders volumes to period with zones percentes finished')
        Logger.debug(__file__, 'Calculated orders volumes: {}'.format(self.configs.orders_volumes))

    def __calculate_orders_volumes_for_generations(self):
        '''
        Calculate orders volumes list for generation
        '''

        Logger.info(__file__, 'Starting calculating orders volumes for generating {} orders'.format(
            self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]
        ))

        in_blue_zone = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_IN_FIRST_BLUE_ZONE]
        not_used = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT] - in_blue_zone

        found = True
        limit = len(self.configs.orders_volumes) - 1

        while found:
            i = limit
            found_volume = False

            while i >= 0 and not found_volume:
                volume = self.configs.orders_volumes[i]
                needed_orders = volume[Values.BLUE_ZONE_VOLUME] + volume[Values.GREEN_ZONE_VOLUME]

                if not_used > 0 and needed_orders <= not_used and volume[Values.RED_ZONE_VOLUME] <= in_blue_zone:
                    in_blue_zone = in_blue_zone - volume[Values.RED_ZONE_VOLUME] + volume[Values.BLUE_ZONE_VOLUME]
                    self.configs.orders_volumes_for_generation.append(volume)
                    not_used -= needed_orders

                    found_volume = True
                else:
                    i -= 1

            if i < 0 and not found_volume:
                found = False

        self.configs.not_used_orders_amount = not_used + in_blue_zone

        Logger.info(__file__, "Calculating orders volumes for each period finished")
        Logger.debug(__file__, 'Calculated {} orders volumes for generations: {}'.format(
            len(self.configs.orders_volumes_for_generation),
            self.configs.orders_volumes_for_generation))

    def __calculate_first_generation_period_start_date(self):
        '''
        Calculate start date of first generation perid
        '''

        Logger.info(__file__, 'Starting calculating start date of first period for generation orders')

        current_date = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        day_of_week = current_date.weekday() + 1

        self.configs.is_current_date_in_trading_period = day_of_week in (1, 2, 5)

        days_to_last_period = day_of_week + 7 - 5 if day_of_week < 5 else day_of_week - 5
        days_to_start_period = days_to_last_period + (7 * (len(self.configs.orders_volumes_for_generation)))
        self.configs.start_date = current_date + datetime.timedelta(days=-days_to_start_period)

        Logger.info(__file__,
                    'Calculating start date of first period for generation orders finished. Start at {}'.format(
                        self.configs.start_date))

    def __execute_prepare_configurations_for_generation(self):
        '''
        Call all function for prepare to generation ordera
        '''

        self.__load_currency_pairs_from_file()
        self.__load_tags_from_file()
        self.__calculate_orders_period_volumes()
        self.__calculate_orders_volumes_for_generations()
        self.__calculate_first_generation_period_start_date()

    def __calculate_avg_values_of_id(self):
        id_sum = 0
        amount = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]

        x = self.configs.settings[Values.ID_GENERATOR][Values.MWC1616_X]
        y = self.configs.settings[Values.ID_GENERATOR][Values.MWC1616_Y]

        for i in range(amount):
            id_sum += IdGenerator().get_next()

        IdGenerator.seed_mwc1616(x, y)

        self.configs.avg_value_of_ids = id_sum / amount


if __name__ == '__main__':
    Logger.add_to_journal(__file__, Level.INFO, 'Program started')

    launcher = Launcher()
    launcher.start()

    Logger.info(__file__, 'Program finished')
