from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
import mysql.connector

from Service.AbstractConnection.Implementation.MySqlConnection import MySqlConnection
from Service.DbService.DbService import DbService


class MySqlService(DbService):
    def __init__(self, user='root', password='', host='127.0.0.1', port='3306', database=''):
        self.__connection = MySqlConnection(user=user, password=password, host=host, port=port, database=database)
        Logger.debug('Created mysql service')

    def execute(self, query, *args, **kwargs):
        try:
            self.__connection.open()

            cursor = self.__connection.get_cursor()

            if cursor is not None:
                try:
                    cursor.execute(query)
                except mysql.connector.Error as err:
                    Logger.error(__file__, err.msg)

                self.__connection.commit()

        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def execute_many(self, queries):
        try:
            self.__connection.open()

            cursor = self.__connection.get_cursor()

            if cursor is not None:

                for query in queries:
                    try:
                        cursor.execute(query)
                    except mysql.connector.Error as err:
                        Logger.error(__file__, err.msg)

                self.__connection.commit()

        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def execute_multiple(self, query, params):
        try:
            self.__connection.open()

            cursor = self.__connection.get_cursor()

            if cursor is not None:
                try:
                    cursor.executemany(query, params)
                except mysql.connector.Error as err:
                    Logger.error(__file__, err.msg)

                self.__connection.commit()

        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)
