from Service.AbstractConnection.AbstractConnection import AbstractConnection
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger

import csv


class CsvFileDescriptor(AbstractConnection):
    def __init__(self, path):
        self.__file = None
        self.path = path
        self.mode = None

    def open(self, path, mode='r'):
        if path is None:
            if self.path is not None:
                raise TypeError('Path parameter of file descriptor must bo not None')
            else:
                path = self.path
        if mode is None:
            raise TypeError('Mode parameter of file descriptor must bo not None')

        try:
            self.__file = open(file=path, mode=mode, newline='')
        except Exception as err:
            Logger.error(__file__, err.__str__())

    def close(self, *args, **kwargs):
        try:
            self.__file.close()
        except Exception as err:
            Logger.error(__file__, err.__str__())

    def is_available(self):
        return self.__file is not None

    def write(self, data):
        writer = csv.writer(self.__file, delimiter=',')
        for line in data:
            writer.writerow(line)

    def read(self):
        reader = csv.reader(self.__file)

        rows = []
        for row in reader:
            rows.append(row)
        return rows
