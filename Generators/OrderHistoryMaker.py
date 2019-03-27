import datetime
import re

from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Generators.GeneralOrderInformationBuilder import GeneralOrderInformationBuilder
from Generators.OrderRecordsBuilder import OrderRecordsBuilder
from Generators.PseudorandomNumberGenerator.Implementation.IdGenerator import IdGenerator
from Generators.PseudorandomNumberGenerator.Implementation.LinearCongruentialGenerator import \
    LinearCongruentialGenerator as LCG
from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Utils.Utils import Utils


class OrderHistoryMaker:
    def __init__(self):
        self.configs = Configuration()
        self.records_builder = OrderRecordsBuilder()
        self.order_builder = GeneralOrderInformationBuilder()

    def __count_volume_by_color(self, color):
        '''
        Calculate total zone orders volume
        :param color: zone color
        :return: total zone orders volume
        '''

        total_volume = 0
        for volume in self.configs.orders_volumes_for_generation:
            total_volume += volume[color]
        return total_volume

    def execute_generation(self):
        '''
        Execute generation orders history
        '''

        Logger.info(__file__, 'Order history making started')

        self.__generate_green_orders()
        #self.__generate_red_blue_orders()

        Logger.info(__file__, 'Order history making finished')

    def __get_order_in_green_zone(self, period):
        '''
        Generate GeneralOrderHistory for green zone
        :param period: period index for generation
        :return: GeneralOrderHistory instance for green zone period
        '''

        return self.records_builder.set_general_order_info(
            self.__generate_general_order_information()
        ).build_order_with_records_in_green_zone(period)

    def __get_order_in_blue_red_zone(self, period_start, period_end):
        '''
        Generate GeneralOrderHistory for blue-red zone
        :param period_start: index of start order period
        :param period_end: index of finish order period
        :return: GeneralOrderHistory instance for blue-red zone period
        '''

        return self.records_builder.set_general_order_info(
            self.__generate_general_order_information()
        ).build_order_with_records_in_blue_red_zone(period_start, period_end)

    def __generate_general_order_information(self):
        '''
        Return GeneralOrderInformation instance with generators values
        :return: GeneralOrderInformation instance
        '''

        return self.order_builder. \
            set_id(IdGenerator.get_next()). \
            set_status_sequence(LCG.get_next(Values.STATUS_SEQUENCE_GENERATOR)). \
            set_currency_pair_by_value(LCG.get_next(Values.CURRENCY_PAIR_GENERATOR)). \
            set_currency_pair_init_value_by_deviation_percent(LCG.get_next(Values.INIT_PX_PERCENT_DEVIATION_GENERATOR)). \
            set_init_volume(LCG.get_next(Values.INIT_VOLUME_GENERATOR)). \
            set_currency_pair_fill_value_by_deviation_percent(LCG.get_next(Values.FILL_PX_PERCENT_DEVIATION_GENERATOR)). \
            set_fill_volume_deviation_percent(LCG.get_next(Values.PARTIAL_FILLED_PERCENT_GENERATOR)). \
            set_fill_volume(). \
            set_statuses_in_blue_zone_by_value(LCG.get_next(Values.BLUE_STATUSES_AMOUNT_GENERATOR)). \
            set_tags_with_description(LCG.get_next(Values.TAGS_GENERATOR_1),
                                      LCG.get_next(Values.TAGS_GENERATOR_2),
                                      LCG.get_next(Values.TAGS_GENERATOR_3),
                                      LCG.get_next(Values.TAGS_GENERATOR_4),
                                      LCG.get_next(Values.TAGS_GENERATOR_5)). \
            build()

    def __generate_green_orders(self):
        '''
        Generate green zone orders records with generators configurations
        '''

        Logger.info(__file__, 'Started generation order history in green zone')

        total_green_volume = int(self.__count_volume_by_color(Values.GREEN_ZONE_VOLUME)) - 1
        period = 1
        period_limit = self.configs.orders_volumes_for_generation[period][Values.GREEN_ZONE_VOLUME]
        period_counter = 0

        for i in range(total_green_volume + 1):
            Logger.debug(__file__, f'Generation {i + 1} green order history started')

            if period_counter <= period_limit:
                period_counter += 1
            else:
                period_counter = 0
                period += 1
                period_limit = self.configs.orders_volumes_for_generation[period - 1][Values.GREEN_ZONE_VOLUME]

            # do something with:
            # self.__get_order_in_green_zone(period).SerializeToString()

            Logger.info(__file__, f'Generation {i + 1} green order history finished')
        Logger.info(__file__, 'Generation green zone orders history finished')

    def __generate_red_blue_orders(self):
        '''
        Generate blue-red zone orders records with generators configurations
        '''

        Logger.info(__file__, 'Started generation order history in blue-red zone')

        period_start = -1
        period_finish = 0
        period_start_limit = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_IN_FIRST_BLUE_ZONE]
        period_start_counter = 1
        period_finish_limit = self.configs.orders_volumes_for_generation[period_finish][Values.RED_ZONE_VOLUME]
        period_finish_counter = 1
        finished_counter = 1
        finished_limit = self.__count_volume_by_color(Values.RED_ZONE_VOLUME)
        total_orders_amount = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]

        total_green_volume = int(self.__count_volume_by_color(Values.GREEN_ZONE_VOLUME)) - 1

        for i in range(total_green_volume + 1, total_orders_amount):
            Logger.debug(__file__, f'Started generation {i - total_green_volume} order history in blue-red zone')

            # do something with:
            # self.__get_order_in_blue_red_zone(period_start, period_finish).SerializeToString()

            Logger.info(__file__, f'Generation {i - total_green_volume} order history in blue-red zone finished')

            if period_start_counter < period_start_limit:
                period_start_counter += 1
            else:
                period_start += 1
                period_start_limit = self.configs.orders_volumes_for_generation[period_start][Values.BLUE_ZONE_VOLUME] \
                    if period_start < len(
                    self.configs.orders_volumes_for_generation) else self.configs.not_used_orders_amount

                if period_start == len(self.configs.orders_volumes_for_generation):
                    period_start = 0

                period_start_counter = 1

            if finished_counter < finished_limit:
                finished_counter += 1

                if period_finish_counter < period_finish_limit:
                    period_finish_counter += 1
                else:
                    period_finish += 1
                    period_finish_limit = self.configs.orders_volumes_for_generation[period_finish][
                        Values.RED_ZONE_VOLUME]
                    period_finish_counter = 1
            else:
                period_finish = -1

        Logger.info(__file__, 'Generation blue-red zone orders history finished')

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

    def execute_prepare_configurations_for_generation(self):
        '''
        Call all function for prepare to generation ordera
        '''

        self.__load_currency_pairs_from_file()
        self.__load_tags_from_file()
        self.__calculate_orders_period_volumes()
        self.__calculate_orders_volumes_for_generations()
        self.__calculate_first_generation_period_start_date()
        self.__calculate_avg_values_of_id()
        self.__register_lcg_generators()

    def __calculate_avg_values_of_id(self):
        '''
        Calculate id's avg value. Need for calc order direction
        '''

        id_sum = 0
        amount = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]

        x = self.configs.settings[Values.ID_GENERATOR][Values.MWC1616_X]
        y = self.configs.settings[Values.ID_GENERATOR][Values.MWC1616_Y]

        for i in range(amount):
            id_sum += IdGenerator().get_next()

        IdGenerator.set_seed(x, y)

        self.configs.avg_value_of_ids = id_sum / amount

    def __register_lcg_generators(self):
        '''
        Register all generators setting to LCG generator
        '''

        for section in self.configs.settings:
            if 'GENERATOR' in section:
                LCG.set_linear_congruential_generator(section, self.configs.settings[section])

