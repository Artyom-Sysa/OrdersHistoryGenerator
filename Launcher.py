import datetime
import os
import threading
import time

from Config.ConfigLoader.ConfigLoader.Implementation.IniFileConfigLoader import IniFileConfigLoader
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Entities.RmqConsumer import RmqConsumer
from Entities.StatisticsDataStorage import StatisticsDataStorage
from Generators.OrderHistoryMaker import OrderHistoryMaker
from Reporter.Implementation.ConsoleReporter import ConsoleReporter
from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Service.LoggerService.Implementation.DefaultPythonLoggingService import LoggingLevel as Level
from Utils.Utils import Utils


class Launcher:
    def start(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Launcher started')
        self.__load_configs()
        self.__execute()
        self.generator_and_publisher_thread = None
        self.consumer_thread = None
        self.generator_and_publisher_event = None
        self.consumer_event = None
        self.report_thread = None


    def __load_configs(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Started load configuration')

        self.configs = Configuration()
        self.config_loader = IniFileConfigLoader()
        self.config_loader.load(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.DEFAULT_SETTING_FILE_PATH])

        Logger.configurate_logger()

        Logger.add_to_journal(__file__, Level.INFO, 'Loading configuration finished')
        Logger.add_to_journal(__file__, Level.DEBUG, 'Loaded configurations :\n{}'.format(self.configs.settings))

    def __execute(self):
        self.generator_and_publisher_event = threading.Event()

        self.history_maker = OrderHistoryMaker(self.generator_and_publisher_event)
        self.history_maker.prepare_configurations_for_generation()

        self.consumer_thread = threading.Thread(target=self.start_consumer)
        self.generator_and_publisher_thread = threading.Thread(target=self.start_orders_history_generation)

        self.generator_and_publisher_thread.start()
        self.consumer_thread.start()

        sec = self.configs.settings[Values.GENERAL_SECTION_NAME][Values.REPORTER_DELAY]
        while not self.generator_and_publisher_event.is_set() or not self.consumer_event.is_set():
            time.sleep(sec)
            self.report()
        self.report()


        Logger.info(__file__, 'Program finished')

    def start_consumer(self):
        self.consumer_event = threading.Event()
        consumer = RmqConsumer(self.consumer_event)
        consumer.consume()

        if len(consumer.consumed_data) > 0:
            consumer.send_consumed_data_to_mysql()



    def report(self):
        Logger.info(__file__, 'Start reporting')
        print('Start getting reporting data at {}'.format(datetime.datetime.now()))
        Utils.get_db_report_date()
        ConsoleReporter.report(StatisticsDataStorage.statistics)
        print('Reporter finished data at {}'.format(datetime.datetime.now()))
        Logger.info(__file__, 'Reporting finished')

    def start_orders_history_generation(self):
        self.history_maker.execute_generation()
        Logger.info(__file__, 'Order history generation finished')


if __name__ == '__main__':
    Logger.add_to_journal(__file__, Level.INFO, 'Program started')

    launcher = Launcher()
    launcher.start()