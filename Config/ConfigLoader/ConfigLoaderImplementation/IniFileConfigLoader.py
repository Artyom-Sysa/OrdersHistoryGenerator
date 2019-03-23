from Config.ConfigLoader.ConfigLoader import ConfigLoader
from Config.Configurations import Configuration
from Utils.Utils import Utils
import configparser


class IniFileConfigLoader(ConfigLoader):
    __sections_names = {
        'GENERAL': 'GENERAL',
        'LOGGER': 'LOGGER'
    }

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

    def write_default(self):
        '''
        Write default settings to file path which passed to load function if file by this don't exisits

        :return: boolean value of success finish writing
        '''

        cfg = configparser.ConfigParser(comment_prefixes=('#', ';', '##'),
                                        allow_no_value=True,
                                        empty_lines_in_values=True)

        cfg.add_section(self.__sections_names['GENERAL'])

        cfg.set(self.__sections_names['GENERAL'], '; General config section')
        cfg.set(self.__sections_names['GENERAL'], '; DO NOT REMOVE ANY VALUES FROM THIS SECTION')
        cfg.set(self.__sections_names['GENERAL'], '; ALL PARAMETER REQUIRED')
        cfg.set(self.__sections_names['GENERAL'], ';')

        cfg.set(self.__sections_names['GENERAL'], '# Total generated orders amount. Must be int')
        cfg.set(self.__sections_names['GENERAL'], 'orders_amount', str(self.configuration.orders_amount))

        cfg.set(self.__sections_names['GENERAL'], '# This parameter is required to calculate the number of trading periods. Must be int')
        cfg.set(self.__sections_names['GENERAL'], 'orders_in_first_blue_zone', str(self.configuration.orders_in_first_blue_zone))

        cfg.set(self.__sections_names['GENERAL'], ';\n; Sum of next three parameters must be 100!\n;')

        cfg.set(self.__sections_names['GENERAL'], '# This value show how many orders start in one of previous periods and finish in current periods. Must be int')
        cfg.set(self.__sections_names['GENERAL'], 'red_zone_orders_percent', str(self.configuration.red_zone_orders_percent))

        cfg.set(self.__sections_names['GENERAL'],
                '# This value show how many orders start and finish in current period. Must be int')
        cfg.set(self.__sections_names['GENERAL'], 'green_zone_orders_percent', str(self.configuration.green_zone_orders_percent))

        cfg.set(self.__sections_names['GENERAL'], '# This value show how many orders start in currenct period and finish in one of next periods. Must be int')
        cfg.set(self.__sections_names['GENERAL'], 'blue_zone_orders_percent', str(self.configuration.blue_zone_orders_percent))

        cfg.set(self.__sections_names['GENERAL'], '# Path to file with currency pairs')
        cfg.set(self.__sections_names['GENERAL'], 'currency_pair_file_path', self.configuration.currency_pair_file_path)

        cfg.set(self.__sections_names['GENERAL'], '# Path to file with tags')
        cfg.set(self.__sections_names['GENERAL'], 'tags_file_path', self.configuration.tags_file_path)

        cfg.set(self.__sections_names['GENERAL'], '# Path to write order history')
        cfg.set(self.__sections_names['GENERAL'], 'order_history_write_file_path', self.configuration.order_history_write_file_path)

        cfg.set(self.__sections_names['GENERAL'], '# This parameter is responsible for deviations from the currency pair value. Must be float/int, greater or equal than 0')
        cfg.set(self.__sections_names['GENERAL'], 'currency_deviation_percent', str(self.configuration.currency_deviation_percent))

        cfg.add_section(self.__sections_names['LOGGER'])
        cfg.set(self.__sections_names['LOGGER'], '; DO NOT REMOVE ANY VALUES FROM THIS SECTION')
        cfg.set(self.__sections_names['LOGGER'], '; ALL PARAMETER REQUIRED')
        cfg.set(self.__sections_names['LOGGER'], ';')

        cfg.set(self.__sections_names['LOGGER'], '# Logger string format. See attributes: https://docs.python.org/3/library/logging.html')
        cfg.set(self.__sections_names['LOGGER'], 'logger_format', self.configuration.logger_format.replace('%', '%%'))

        cfg.set(self.__sections_names['LOGGER'], '; Logger datetime format')
        cfg.set(self.__sections_names['LOGGER'], 'logger_date_format', self.configuration.logger_date_format.replace('%', '%%'))

        cfg.set(self.__sections_names['LOGGER'], '; Logging level. Available values: CRITICAL, FATAL. ERROR, WARN, INFO, DEBUG, NOTSET')
        cfg.set(self.__sections_names['LOGGER'], 'logger_level', self.configuration.logger_level)

        try:
            with open(self.file_path, 'w') as cfg_file:
                cfg.write(cfg_file)
        except:
            return False
        return True
