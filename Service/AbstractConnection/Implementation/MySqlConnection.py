import abc
import time

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

        self.__open_conn()
        if not self.is_available():
            self.reconnect()
        else:

            Logger.debug(__file__, 'Created mysql connection with params {} {} {} {}'.format(self.__user,
                                                                                             self.__password,
                                                                                             self.__host,
                                                                                             self.__database))

    def __open_conn(self):
        try:
            self.__conn = None
            self.__conn = mysql.connector.connect(user=self.__user,
                                                  password=self.__password,
                                                  host=self.__host,
                                                  port=self.__port,
                                                  database=self.__database)
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def close(self, *args, **kwargs):
        try:
            self.__conn.close()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def is_available(self):
        try:
            return self.__conn.is_connected()
        except:
            return False

    def get_cursor(self):
        try:
            return self.__conn.cursor()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)
            if not self.is_available():
                self.reconnect()
                self.get_cursor()

    def commit(self):
        try:
            self.__conn.commit()
            return True
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)
            self.rollback()
            return False

    def rollback(self):
        try:
            self.__conn.rollback()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def reconnect(self):
        while True:
            self.__open_conn()
            if not self.is_available():
                time.sleep(1)
            else:
                break
