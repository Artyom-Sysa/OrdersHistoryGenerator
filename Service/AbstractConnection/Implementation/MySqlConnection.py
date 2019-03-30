import abc

import mysql.connector
from Service.AbstractConnection.AbstractConnection import AbstractConnection
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
from Service.LoggerService.Implementation.DefaultPythonLoggingService import LoggingLevel as Level
from Utils.Utils import Utils


class MySqlConnection(AbstractConnection):
    def __init__(self, user='root', password='', host='127.0.0.1', port='3306', database=''):
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port
        self.__database = database
        self.__conn = None

    def open(self):
        try:
            self.__conn = mysql.connector.connect(user=self.__user,
                                                  password=self.__password,
                                                  host=self.__host,
                                                  port=self.__port,
                                                  database=self.__database)

            Logger.debug('Created mysql connection with params {} {} {} {}'.format(self.__user,
                                                                                   self.__password,
                                                                                   self.__host,
                                                                                   self.__database))
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def close(self, *args, **kwargs):
        try:
            self.__conn.close()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def is_available(self):
        return self.__conn.is_connected()

    def get_cursor(self):
        try:
            return self.__conn.cursor()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)
        return None

    def commit(self):
        try:
            self.__conn.commit()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)
            self.rollback()

    def rollback(self):
        try:
            self.__conn.rollback()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)
