from Config.ConfigLoader.ConfigLoader import ConfigLoader
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
from Utils.Utils import Utils
from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import LoggingLevel as Level

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

        Logger.add_to_journal(__file__, Level.INFO, 'Start execution loading configs function')

        self.file_path = file_path

        Logger.add_to_journal(__file__, Level.DEBUG, 'File path with configurations: {}'.format(self.file_path))

        if not Utils.is_file_exists(self.file_path):
            Logger.add_to_journal(__file__, Level.INFO, 'File by path {} not exists'.format(self.file_path))
            self.write_default()
        else:
            self.read_data_from_file(file_path)

    def write_default(self):
        '''
        Write default settings to file path which passed to load function if file by this don't exisits

        :return: boolean value of success finish writing
        '''

        Logger.add_to_journal(__file__, Level.INFO,'Start execution function of writing configs to file {}'.format(self.file_path))

        cfg = configparser.ConfigParser(comment_prefixes=('#', ';'),
                                        allow_no_value=True,
                                        empty_lines_in_values=True)

        Logger.add_to_journal(__file__,
                              Level.DEBUG,
                              'Creating section with name {}'.format(Values.GENERAL_SECTION_NAME))

        cfg.add_section(Values.GENERAL_SECTION_NAME)

        cfg.set(Values.GENERAL_SECTION_NAME, '; General config section')
        cfg.set(Values.GENERAL_SECTION_NAME, '; DO NOT REMOVE ANY VALUES FROM THIS SECTION')
        cfg.set(Values.GENERAL_SECTION_NAME, '; ALL PARAMETER REQUIRED')
        cfg.set(Values.GENERAL_SECTION_NAME, ';')

        cfg.set(Values.GENERAL_SECTION_NAME, '# Total generated orders amount. Must be int')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME,
                             Values.ORDERS_AMOUNT,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_AMOUNT])

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This parameter is required to calculate the number of trading periods. Must be int')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.ORDERS_IN_FIRST_BLUE_ZONE,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.ORDERS_IN_FIRST_BLUE_ZONE])

        cfg.set(Values.GENERAL_SECTION_NAME, ';\n; Sum of next three parameters must be 100!\n;')

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This value show how many orders start in one of previous periods and finish in current periods. Must be int')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.RED_ZONE_ORDERS_PERCENT,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.RED_ZONE_ORDERS_PERCENT])

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This value show how many orders start and finish in current period. Must be int')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.GREEN_ZONE_ORDERS_PERCENT,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.GREEN_ZONE_ORDERS_PERCENT])

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This value show how many orders start in currenct period and finish in one of next periods. Must be int')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.BLUE_ZONE_ORDERS_PERCENT,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.BLUE_ZONE_ORDERS_PERCENT])

        cfg.set(Values.GENERAL_SECTION_NAME, '# Path to file with currency pairs')

        self.__add_parameter(cfg, Values.GENERAL_SECTION_NAME, Values.CURRENCY_PAIRS_FILE_PATH,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_PAIRS_FILE_PATH])

        cfg.set(Values.GENERAL_SECTION_NAME, '# Path to file with tags')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.TAGS_FILE_PATH,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.TAGS_FILE_PATH])

        cfg.set(Values.GENERAL_SECTION_NAME, '# Path to write order history')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.ORDER_HISTORY_WRITE_FILE_PATH,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.ORDER_HISTORY_WRITE_FILE_PATH])

        cfg.set(Values.GENERAL_SECTION_NAME,
                '# This parameter is responsible for deviations from the currency pair value. Must be float/int, greater or equal than 0')

        self.__add_parameter(cfg,
                             Values.GENERAL_SECTION_NAME, Values.CURRENCY_DEVIATION_PERCENT,
                             self.configuration.settings[Values.GENERAL_SECTION_NAME][Values.CURRENCY_DEVIATION_PERCENT])

        Logger.add_to_journal(__file__,
                              Level.DEBUG,
                              'Creating section with name {}'.format(Values.LOGGER_SECTION_NAME))

        cfg.add_section(Values.LOGGER_SECTION_NAME)
        cfg.set(Values.LOGGER_SECTION_NAME, '; DO NOT REMOVE ANY VALUES FROM THIS SECTION')
        cfg.set(Values.LOGGER_SECTION_NAME, '; ALL PARAMETER REQUIRED')
        cfg.set(Values.LOGGER_SECTION_NAME, ';')

        cfg.set(Values.LOGGER_SECTION_NAME, '# Folder path to logging files')

        self.__add_parameter(cfg,
                             Values.LOGGER_SECTION_NAME, Values.LOGGING_FOLDER_PATH,
                             self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH])

        cfg.set(Values.LOGGER_SECTION_NAME,
                '# Logger string format. See attributes: https://docs.python.org/3/library/logging.html')

        self.__add_parameter(cfg,
                             Values.LOGGER_SECTION_NAME, Values.LOGGER_FORMAT,
                             self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%', '%%'))

        cfg.set(Values.LOGGER_SECTION_NAME, '# Logger datetime format')

        self.__add_parameter(cfg, Values.LOGGER_SECTION_NAME, Values.LOGGER_DATE_FORMAT,
                             self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%', '%%'))

        cfg.set(Values.LOGGER_SECTION_NAME,
                '# Logging level. Available values: CRITICAL, FATAL. ERROR, WARN, INFO, DEBUG, NOTSET')

        self.__add_parameter(cfg,
                             Values.LOGGER_SECTION_NAME, Values.LOGGER_LEVEL,
                             self.configuration.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])

        for section in self.configuration.settings:
            if section not in [Values.GENERAL_SECTION_NAME, Values.LOGGER_SECTION_NAME]:
                Logger.add_to_journal(__file__, Level.DEBUG,
                                      'Creating section with name {}'.format(section))

                cfg[section] = self.configuration.settings[section]

                Logger.add_to_journal(__file__,
                                      Level.DEBUG,
                                      'Set data: {} to section {}'.format(self.configuration.settings[section],
                                                                          section))

        try:
            Logger.add_to_journal(__file__, Level.INFO, 'Try write configs to file {}'.format(self.file_path))

            with open(self.file_path, 'w') as cfg_file:
                cfg.write(cfg_file)

            Logger.add_to_journal(__file__, Level.INFO, 'Writing finished successfully'.format(self.file_path))
        except:
            Logger.add_to_journal(__file__, Level.INFO, 'Writing finished with exception'.format(self.file_path))
            Logger.add_to_journal(__file__,
                                  Level.INFO,
                                  'Execution function of writing configs to file {} finished'.format(self.file_path))

            return False
        Logger.add_to_journal(__file__, Level.INFO,
                              'Execution function of writing configs to file {} finished'.format(
                                  self.file_path))
        return True

    def read_data_from_file(self, file_path):
        '''
        Read configurations from ini file with 'file_path' path and
        save it to configuration dictionary

        :param file_path: path to ini file with programm configurations
        '''

        Logger.add_to_journal(__file__, Level.INFO,
                              'Start execution reading config file by path {}'.format(self.file_path))

        cfg_parser = configparser.ConfigParser(comment_prefixes=('#', ';'),
                                               allow_no_value=True,
                                               empty_lines_in_values=True)
        try:
            cfg_parser.read(file_path)

            Logger.add_to_journal(__file__,
                                  Level.INFO,
                                  'Data from file {} loaded to configparser'.format(self.file_path))

            Logger.add_to_journal(__file__, Level.INFO, 'Start writing data to configuration object')
            for section in cfg_parser.sections():
                Logger.add_to_journal(__file__,
                                      Level.INFO,
                                      'Writing {} section to configuration object'.format(section))

                for key in cfg_parser[section]:
                    _, value = Utils.is_number(cfg_parser.get(section, key))
                    self.configuration.settings[section][key] = value
                    Logger.add_to_journal(__file__, Level.DEBUG, 'Parameter {} set to value {}'.format(key, value))

            Logger.add_to_journal(__file__, Level.INFO, 'Writing data to configuration object  successfully finished')
        except:
            Logger.add_to_journal(__file__,
                                  Level.WARNING,
                                  'Writing data to configuration object  finished with exception. Some or full setting from file can be not setted to configuration object')

    def __add_parameter(self, cfg_parser, section_name, parameter_name, value):
        cfg_parser.set(section_name, parameter_name, str(value))

        Logger.add_to_journal(__file__,
                              Level.DEBUG,
                              "Added parameter '{}' to section {} with value: {}".format(parameter_name,
                                                                                         section_name,
                                                                                         value))
