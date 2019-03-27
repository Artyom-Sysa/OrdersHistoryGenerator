from Service.AbstractConnection.AbstractConnection import AbstractConnection
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger


class FileDescriptor(AbstractConnection):
    def __init__(self, path):
        self.__file = None
        self.path = path
        self.mode = None

    def open(self, path, mode='r'):
        if path is None:
            if self.path is not None:
                raise Exception('Path parameter of file descriptor must bo not None')
            else:
                path = self.path
        if mode is None:
            raise Exception('Mode parameter of file descriptor must bo not None')

        try:
            self.__file = open(file=path, mode=mode)
        except Exception as err:
            Logger.error(__file__, err.__str__())

    def close(self, *args, **kwargs):
        try:
            self.__file.close()
        except Exception as err:
            Logger.error(__file__, err.__str__())

    def is_available(self):
        pass

    def write(self, data):
        try:
            self.__file.write(data)
        except Exception as err:
            Logger.error(__file__, err.__str__())
