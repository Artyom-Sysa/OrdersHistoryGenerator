from Config.ConfigLoader.ConfigLoader.Implementation.IniFileConfigLoader import IniFileConfigLoader
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
#from Generators.OrderHistoryMaker import OrderHistoryMaker
from Generators.OrderHistoryMaker import OrderHistoryMaker
from Service.LoggerService.Implementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger
from Service.LoggerService.Implementation.DefaultPythonLoggingService import LoggingLevel as Level


class Launcher:
    def start(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Launcher started')
        self.__load_configs()
        self.__execute_generation_order_history()

    def __load_configs(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Started load configuration')

        self.configs = Configuration()
        self.config_loader = IniFileConfigLoader()
        self.config_loader.load(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.DEFAULT_SETTING_FILE_PATH])

        Logger.configurate_logger()

        Logger.add_to_journal(__file__, Level.INFO, 'Loading configuration finished')
        Logger.add_to_journal(__file__, Level.DEBUG, 'Loaded configurations :\n{}'.format(self.configs.settings))

    def __execute_generation_order_history(self):
        history_maker = OrderHistoryMaker()
        history_maker.prepare_configurations_for_generation()
        history_maker.execute_generation()


if __name__ == '__main__':
    Logger.add_to_journal(__file__, Level.INFO, 'Program started')

    launcher = Launcher()
    launcher.start()

    Logger.info(__file__, 'Program finished')
