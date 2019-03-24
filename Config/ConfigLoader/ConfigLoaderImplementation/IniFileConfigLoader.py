from Config.ConfigLoader.ConfigLoader import ConfigLoader
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Utils.Utils import Utils

import configparser


class IniFileConfigLoader(ConfigLoader):

    def __init__(self):
        self.configuration = Configuration()

    def load(self, file_path):
        '''
        Load configurations from file with passed path

        :param file_path: path to file with configurations
        :return: boolean value of success loading configurations
        '''

        self.file_path = file_path

        if not Utils.is_file_exists(self.file_path):
            self.write_default()
        else:
            self.read_data_from_file(file_path)

    def write_default(self):
        '''
        Write default settings to file path which passed to load function if file by this don't exisits

        :return: boolean value of success finish writing
        '''

        cfg = configparser.ConfigParser(comment_prefixes=('#', ';'),
                                        allow_no_value=True,
                                        empty_lines_in_values=True)

        cfg.add_section(self.__sections_names['GENERAL'])

        cfg.set(Values.GENERAL_SECTION_NAME, '; General config section')
        cfg.set(Values.GENERAL_SECTION_NAME, '; DO NOT REMOVE ANY VALUES FROM THIS SECTION')
        cfg.set(Values.GENERAL_SECTION_NAME, '; ALL PARAMETER REQUIRED')
        cfg.set(Values.GENERAL_SECTION_NAME, ';')

        cfg.set(Values.GENERAL_SECTION_NAME, '# Total generated orders amount. Must be int')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.ORDERS_AMOUNT,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT]))

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This parameter is required to calculate the number of trading periods. Must be int')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.ORDERS_IN_FIRST_BLUE_ZONE,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_IN_FIRST_BLUE_ZONE]))

        cfg.set(Values.GENERAL_SECTION_NAME, ';\n; Sum of next three parameters must be 100!\n;')

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This value show how many orders start in one of previous periods and finish in current periods. Must be int')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.RED_ZONE_ORDERS_PERCENT,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.RED_ZONE_ORDERS_PERCENT]))

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This value show how many orders start and finish in current period. Must be int')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.GREEN_ZONE_ORDERS_PERCENT,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.GREEN_ZONE_ORDERS_PERCENT]))

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This value show how many orders start in currenct period and finish in one of next periods. Must be int')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.BLUE_ZONE_ORDERS_PERCENT,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.BLUE_ZONE_ORDERS_PERCENT]))

        cfg.set(Values.GENERAL_SECTION_NAME, '# Path to file with currency pairs')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.CURRENCY_PAIRS_FILE_PATH,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH]))

        cfg.set(Values.GENERAL_SECTION_NAME, '# Path to file with tags')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.TAGS_FILE_PATH,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH]))

        cfg.set(Values.GENERAL_SECTION_NAME, '# Path to write order history')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.ORDER_HISTORY_WRITE_FILE_PATH,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.ORDER_HISTORY_WRITE_FILE_PATH]))

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This parameter is responsible for deviations from the currency pair value. Must be float/int, greater or equal than 0')
        cfg.set(Values.GENERAL_SECTION_NAME, Values.CURRENCY_DEVIATION_PERCENT,
                str(self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_DEVIATION_PERCENT]))

        cfg.add_section(Values.LOGGER_SECTION_NAME)
        cfg.set(Values.LOGGER_SECTION_NAME, '; DO NOT REMOVE ANY VALUES FROM THIS SECTION')
        cfg.set(Values.LOGGER_SECTION_NAME, '; ALL PARAMETER REQUIRED')
        cfg.set(Values.LOGGER_SECTION_NAME, ';')

        cfg.set(Values.LOGGER_SECTION_NAME,
                '# Logger string format. See attributes: https://docs.python.org/3/library/logging.html')
        cfg.set(Values.LOGGER_SECTION_NAME, Values.LOGGER_FORMAT,
                self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%', '%%'))

        cfg.set(Values.LOGGER_SECTION_NAME, '# Logger datetime format')
        cfg.set(Values.LOGGER_SECTION_NAME, Values.LOGGER_DATE_FORMAT,
                self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%', '%%'))

        cfg.set(Values.LOGGER_SECTION_NAME,
                '# Logging level. Available values: CRITICAL, FATAL. ERROR, WARN, INFO, DEBUG, NOTSET')
        cfg.set(Values.LOGGER_SECTION_NAME, Values.LOGGER_LEVEL,
                str(self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL]))

        for section in self.configuration.settings:
            if section not in [Values.GENERAL_SECTION_NAME, Values.LOGGER_SECTION_NAME]:
                cfg[section] = self.configuration.settings[section]

        try:
            with open(self.file_path, 'w') as cfg_file:
                cfg.write(cfg_file)
        except:
            return False
        return True

    def read_data_from_file(self, file_path):
        '''
        Read configurations from ini file with 'file_path' path and
        save it to configuration dictionary

        :param file_path: path to ini file with programm configurations
        '''

        cfg_parser = configparser.ConfigParser(comment_prefixes=('#', ';'),
                                               allow_no_value=True,
                                               empty_lines_in_values=True)
        try:
            cfg_parser.read(file_path)

            for section in cfg_parser.sections():
                for key in cfg_parser[section]:
                    _, value = Utils.is_number(cfg_parser.get(section, key))
                    self.configuration.settings[section][key] = value
        except:
            pass
