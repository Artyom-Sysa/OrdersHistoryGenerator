import abc


class LoggerService(abc.ABC):
    '''
    List for saving log items if you don't want execute writing some logs
    before call 'log' function

    In this project uses for saving logs item and execute writing them
    after finishing configuration python in-build logger
    '''
    __journal = []

    @classmethod
    @abc.abstractmethod
    def add_to_journal(cls, logger_file_path, level, message, *args, **kwargs):
        '''
        Add log item to journal buffer

        :param logger_file_path: file from where called this method
        :param level: logging level
        :param message: logging message
        '''
        pass

    @classmethod
    @abc.abstractmethod
    def log(cls, logger_file_path, level, message, *args, **kwargs):
        '''
        Call execute logging for concrete logger with 'level' and 'message'

        :param logger_file_path: file from where called this method
        :param level: logging level
        :param message: logging message
        :return:
        '''
        pass
