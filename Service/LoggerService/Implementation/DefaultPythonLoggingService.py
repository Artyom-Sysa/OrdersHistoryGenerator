import logging
import logging.config
import logging.handlers

import os
from enum import IntEnum
from Utils.Utils import Utils
from Service.LoggerService.LoggerService import LoggerService
from Config.Configurations import ValuesNames as Values
from Config.Configurations import Configuration
import re


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
            logging.getLogger().log(log_item[cls.__LOGGING_LEVEL].value,
                                    log_item[cls.__LOGGING_MESSAGE])
        cls.__journal.clear()

        if level.value not in logging._levelToName:
            level = LoggingLevel.NOTSET

        file = Utils.get_file_name(Utils.get_file_name(logger_file_path))

        logging.getLogger().log(level, "[{}] {}".format(file, message))

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

        Utils.create_folder_if_not_exists(os.path.join(Utils.get_project_root_path(), 'Log'))
        logging_settings_file_path = Configuration().settings[Values.LOGGER_SECTION_NAME][Values.LOGGING_CONF_FILE_PATH]

        logging.config.fileConfig(logging_settings_file_path)

        logger = logging.getLogger()

        for handler_indx in range(0, len(logger.handlers)):
            if isinstance(logger.handlers[handler_indx], logging.handlers.RotatingFileHandler):
                path = logger.handlers[handler_indx].baseFilename
                path_parts = os.path.splitext(path)
                logger.handlers[handler_indx].baseFilename = path_parts[0] + " " \
                                                             + Utils.get_current_date_with_format() + \
                                                             path_parts[1]

                if os.path.exists(path) and os.path.getsize(path) > 0:
                    logger.handlers[handler_indx].doRollover()

        cls.add_to_journal(__file__, LoggingLevel.INFO, 'Execution function of configuration logger finished')
