from Config.ConfigLoader.ConfigLoader.Implementation.IniFileConfigLoader import IniFileConfigLoader
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
# from Generators.OrderHistoryMaker import OrderHistoryMaker
from Generators.OrderHistoryMaker import OrderHistoryMaker
from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Service.LoggerService.Implementation.DefaultPythonLoggingService import LoggingLevel as Level
from Reporter.Implementation.ConsoleReporter import ConsoleReporter
from Entities.StatisticsDataStorage import StatisticsDataStorage


class Launcher:
    def start(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Launcher started')
        self.__load_configs()
        self.__execute()

    def __load_configs(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Started load configuration')

        self.configs = Configuration()
        self.config_loader = IniFileConfigLoader()
        self.config_loader.load(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.DEFAULT_SETTING_FILE_PATH])

        Logger.configurate_logger()

        Logger.add_to_journal(__file__, Level.INFO, 'Loading configuration finished')
        Logger.add_to_journal(__file__, Level.DEBUG, 'Loaded configurations :\n{}'.format(self.configs.settings))

    def __execute(self):
        history_maker = OrderHistoryMaker()
        history_maker.prepare_configurations_for_generation()
        print('Generating orders records history...')
        history_maker.execute_generation()
        print('Writing records to file...')
        history_maker.write_to_file()
        print('Reading records from file...')
        history_maker.read_from_file()
        print('Sending records to RabbitMQ...')
        history_maker.send_readed_records_to_rmq()
        print('Sending records to MySQL...')
        history_maker.send_readed_records_to_mysql()

        ConsoleReporter.report(StatisticsDataStorage.statistics)


if __name__ == '__main__':
    Logger.add_to_journal(__file__, Level.INFO, 'Program started')

    launcher = Launcher()
    launcher.start()

    Logger.info(__file__, 'Program finished')
