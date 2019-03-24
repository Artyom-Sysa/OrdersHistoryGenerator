import logging
import os

from Config.Configurations import Configuration
from Config.ConfigLoader.ConfigLoaderImplementation.IniFileConfigLoader import IniFileConfigLoader
from Config.Configurations import ValuesNames as Values
from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import LoggingLevel as Level

from Utils.Utils import Utils


class Launcher:
    def start(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Launcher started')
        self.__load_configs()
        self.__configurate_logger()


    def __load_configs(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Started load configuration')

        self.configs = Configuration()
        self.config_loader = IniFileConfigLoader()
        self.config_loader.load(self.configs.settings[Values.GENERAL_SECTION_NAME][Values.DEFAULT_SETTING_FILE_PATH])

        Logger.add_to_journal(__file__, Level.INFO, 'Loading configuration finished')
        Logger.add_to_journal(__file__, Level.DEBUG, 'Loaded configurations :\n{}'.format(self.configs.settings))

    def __configurate_logger(self):
        Logger.add_to_journal(__file__, Level.INFO, 'Start execution function of configuration logger')


        logging.basicConfig(filename=os.path.join(self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH], Utils.get_current_date_with_format() + ".log"),
                            filemode='a',
                            format=self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%%', '%'),
                            datefmt=self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%%', '%'),
                            level=self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])

        Logger.add_to_journal(__file__, Level.INFO, 'Execution function of configuration logger finished')
        Logger.debug(__file__, 'Logger configurated with values: filename: {} | filemode: {} | format: {} | datefmt: {} | level: {}'.format(
            os.path.join(self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH], Utils.get_current_date_with_format() + ".log"),
            'a', self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%', '%%'),
            self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%', '%%'),
            self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])
                                     )


        Utils.create_folder_if_not_exists(self.configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH])




if __name__ == '__main__':
    Logger.add_to_journal(__file__, Level.INFO, 'Program started')

    launcher = Launcher()
    launcher.start()

    Logger.info(__file__, 'Program finished')
