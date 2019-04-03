from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
import mysql.connector

from Service.AbstractConnection.Implementation.MySqlConnection import MySqlConnection
from Service.DbService.DbService import DbService


class MySqlService(DbService):
    def __init__(self, user='root', password='', host='127.0.0.1', port='3306', database=''):
        self.__connection = MySqlConnection(user=user, password=password, host=host, port=port, database=database)

        Logger.debug(__file__, 'Created mysql service')

    def execute(self, query, *args, **kwargs):
        try:
            if not self.__connection.is_available():
                self.__connection.open()

            cursor = self.__connection.get_cursor()

            if cursor is not None:
                Logger.debug(__file__, 'Executing query:{}'.format(query))
                cursor.execute(query)

                self.__connection.commit()
        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def execute_many(self, queries):
        try:
            if not self.__connection.is_available():
                self.__connection.open()

            cursor = self.__connection.get_cursor()
            Logger.debug(__file__, 'Executing many queries started')

            if cursor is not None:
                for query in queries:
                    Logger.debug(__file__, 'Executing query:{}'.format(query))
                    cursor.execute(query)

                self.__connection.commit()

        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

        Logger.debug(__file__, 'Executing many queries finished')

    def execute_multiple(self, query, params):
        try:
            if not self.__connection.is_available():
                self.__connection.open()

            cursor = self.__connection.get_cursor()

            if cursor is not None:
                cursor.executemany(query, params)

                self.__connection.commit()

        except mysql.connector.Error as err:
            Logger.error(__file__, err.msg)

    def close_connection(self):
        Logger.debug(__file__, 'Closing MySQL connection')
        self.__connection.close()

    def open_connection(self):
        Logger.debug(__file__, 'Opening MySQL connection')
        self.__connection.open()
