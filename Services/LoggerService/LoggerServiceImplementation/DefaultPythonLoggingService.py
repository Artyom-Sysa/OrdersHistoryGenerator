import logging
from enum import IntEnum
from Utils.Utils import Utils
from Services.LoggerService.LoggerService import LoggerService


'''
Enum of Logging levels
Duplicate python in-build logging levels
'''
class LoggingLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    FATAL = logging.FATAL
    ERROR = logging.ERROR
    WARN = logging.WARN
    WARNING = logging.WARNING
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
    def warning(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.WARNING, message)

    @classmethod
    def info(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.INFO, message)

    @classmethod
    def debug(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.DEBUG, message)

    @classmethod
    def notset(cls, logger_file_path, message):
        cls.log(logger_file_path, LoggingLevel.NOTSET, message)
