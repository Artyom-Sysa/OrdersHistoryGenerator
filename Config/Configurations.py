from Decorators.Decorators import singleton
import os
from Utils.Utils import Utils


@singleton
class Configuration:
    def __init__(self):
        self.orders_amount = 2000
        self.orders_in_first_blue_zone = 3
        self.red_zone_orders_percent = 15
        self.green_zone_orders_percent = 60
        self.blue_zone_orders_percent = 25
        self.currency_deviation_percent = 5

        self.logging_folder_path = os.path.join(Utils.get_project_root_path(), 'Logs')
        self.logger_format = '%(levelname)s	%(asctime)s.%(msecs)d   %(name)s : %(message)s'
        self.logger_date_format = '%d-%m-%Y %H:%M:%S'
        self.logger_level = 'DEBUG'

        self.order_history_write_file_path = os.path.join(Utils.get_project_root_path(), 'Resources', 'Result.csv')
        self.currency_pair_file_path = os.path.join(Utils.get_project_root_path(), 'Resources', 'CurrencyPairs.txt')
        self.tags_file_path = os.path.join(Utils.get_project_root_path(), 'Resources', 'Tags.txt')
        self.default_setting_file_path = os.path.join(Utils.get_project_root_path(), 'Resources', 'settings.ini')
