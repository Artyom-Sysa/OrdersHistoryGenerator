import logging
import os
from enum import IntEnum
from Utils.Utils import Utils
from Service.LoggerService.LoggerService import LoggerService
from Config.Configurations import ValuesNames as Values
from Config.Configurations import Configuration


class LoggingLevel(IntEnum):
    '''
    Enum of Logging levels
    Duplicate python in-build logging levels
    '''

    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARN = logging.WARN
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NOTSET = logging.NOTSET


class DefaultPythonLoggingService(LoggerService):
    '''
    List for saving log items if you don't want execute writing some logs
    before call 'log' function

    In this project uses for saving logs item and execute writing them
    after finishing configuration python in-build logger
    '''
    __journal = []


    '''
    String name of keys for journal items
    '''
    __LOGGER_NAME = 'logger_name'
    __LOGGING_LEVEL = 'level'
    __LOGGING_MESSAGE = 'messaage'

    @classmethod
    def add_to_journal(cls, logger_file_path, level, message):
        if level.value not in logging._levelToName:
            level = LoggingLevel.NOTSET

        cls.__journal.append({
            cls.__LOGGER_NAME: Utils.get_file_name(Utils.get_file_name(logger_file_path)),
            cls.__LOGGING_LEVEL: level,
            cls.__LOGGING_MESSAGE: message,
        })

    @classmethod
    def log(cls, logger_file_path, level, message):
        '''
        Call execute logging for concrete logger with 'level' and 'message'
        Before executing writing new log-item start writing log items from journal

        :param logger_file_path: file from where called this method
        :param level: logging level
        :param message: logging message
        '''
        for log_item in cls.__journal:
            logging.getLogger(log_item[cls.__LOGGER_NAME]).log(log_item[cls.__LOGGING_LEVEL].value,
                                                               log_item[cls.__LOGGING_MESSAGE])
        cls.__journal.clear()

        if level.value not in logging._levelToName:
            level = LoggingLevel.NOTSET

        logging.getLogger(Utils.get_file_name(Utils.get_file_name(logger_file_path))).log(level, message)

    @classmethod
    def critical(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.CRITICAL, message)

    @classmethod
    def fatal(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.FATAL, message)

    @classmethod
    def error(cls, logger_file_path, message, *args, **kwargs):
        cls.log(logger_file_path, LoggingLevel.ERROR, message)

    @classmethod
    def warn(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.WARN, message)

    @classmethod
    def info(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.INFO, message)

    @classmethod
    def debug(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.DEBUG, message)

    @classmethod
    def notset(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.NOTSET, message)

    @classmethod
    def configurate_logger(cls):
        '''
        Configuration python in-build logger with config object parameters
        '''

        configs = Configuration()

        cls.add_to_journal(__file__, LoggingLevel.INFO, 'Start execution function of configuration logger')

        logging.basicConfig(
            filename=os.path.join(configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH],
                                  Utils.get_current_date_with_format() + ".log"),
            filemode='a',
            format=configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%%', '%'),
            datefmt=configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%%', '%'),
            level=configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])

        cls.add_to_journal(__file__, LoggingLevel.INFO, 'Execution function of configuration logger finished')
        cls.debug(__file__,
                     'Logger configurated with values: filename: {} | filemode: {} | format: {} | datefmt: {} | level: {}'.format(
                         os.path.join(configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH],
                                      Utils.get_current_date_with_format() + ".log"),
                         'a',
                         configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_FORMAT].replace('%', '%%'),
                         configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_DATE_FORMAT].replace('%',
                                                                                                              '%%'),
                         configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGER_LEVEL])
                     )

        Utils.create_folder_if_not_exists(configs.settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_FOLDER_PATH])

