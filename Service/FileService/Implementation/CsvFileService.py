from Service.AbstractConnection.Implementation.CsvFileDescriptor import CsvFileDescriptor
from Service.FileService.FileService import FileService
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger

import csv


class CsvFileService(FileService):
    def __init__(self, path):
        self.__file_descriptor = CsvFileDescriptor(path)
        self.path = path

    def read(self, *args, **kwargs):
        if self.__file_descriptor.mode != 'r':
            self.__file_descriptor.close()
            self.__file_descriptor.open(path=self.path, mode='r')

        return self.__file_descriptor.read()

    def write(self, data, mode, *args, **kwargs):
        if self.__file_descriptor.mode != mode:
            self.__file_descriptor.close()
            self.__file_descriptor.open(path=self.path, mode=mode)

        self.__file_descriptor.write(data)

    def close(self):
        Logger.debug(__file__, 'Closing csv file service')
        self.__file_descriptor.close()

    def open_descriptor(self, mode):
        if self.__file_descriptor.mode != mode:
            self.__file_descriptor.open(path=self.path, mode=mode)
