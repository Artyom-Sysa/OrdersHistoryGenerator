import time

import pika

from Service.AbstractConnection.AbstractConnection import AbstractConnection
from pika import exceptions
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
from pika.spec import BasicProperties


class RmqConnection(AbstractConnection):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.__user = None
        self.__password = None
        self.__host = None
        self.__port = None
        self.__virtual_host = None
        self.exchanges_bindings = dict()
        self.consume_info = dict()

    def open(self, user=pika.connection.Parameters.DEFAULT_USERNAME,
             password=pika.connection.Parameters.DEFAULT_PASSWORD,
             host=pika.connection.Parameters.DEFAULT_PORT,
             port=pika.connection.Parameters.DEFAULT_PORT,
             virtual_host=pika.connection.Parameters.DEFAULT_VIRTUAL_HOST):
        try:

            self.__user = user
            self.__password = password
            self.__host = host
            self.__port = port
            self.__virtual_host = virtual_host
            credentials = pika.PlainCredentials(username=user, password=password)
            params = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials)

            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()


        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)
            return None

    def close(self, *args, **kwargs):
        try:
            if self.connection.is_open:
                self.close()
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def is_available(self):
        try:
            return self.connection.is_open
        except:
            return False

    def declare_exchange(self, exchange_name,
                         exchange_type,
                         passive=False,
                         durable=True,
                         auto_delete=False):
        try:
            self.exchanges_bindings[exchange_name] = list()
            self.exchanges_bindings[exchange_name].append(exchange_type)

            return self.channel.exchange_declare(exchange=exchange_name,
                                                 exchange_type=exchange_type.value,
                                                 passive=passive,
                                                 durable=durable,
                                                 auto_delete=auto_delete)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def declare_queue(self, queue_name, durable=True,exclusive=False, auto_delete=False):
        try:
            return self.channel.queue_declare(queue=queue_name, durable=durable,exclusive=exclusive,auto_delete=auto_delete)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def queue_bind(self, queue_name, exchange_name, routing_key=None):
        self.exchanges_bindings[exchange_name].append(queue_name)

        try:
            return self.channel.queue_bind(queue_name, exchange_name, routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def queue_unbind(self, queue_name, exchange_name, routing_key=None):
        try:
            return self.channel.queue_unbind(queue_name, exchange_name, routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def queue_purge(self, queue_name):
        try:
            return self.channel.queue_purge(queue_name)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def queue_delete(self, queue_name, if_unused=False, if_empty=False):
        try:
            return self.channel.queue_delete(queue_name, if_unused=if_unused, if_empty=if_empty)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def exchange_delete(self, exchange_name=None, if_unused=False):
        try:
            return self.channel.exchange_delete(exchange=exchange_name, if_unused=if_unused)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def exchange_bind(self, destination, source, routing_key=''):
        try:
            return self.channel.exchange_bind(destination=destination, source=source,
                                              routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def exchange_unbind(self, destination, source, routing_key=''):
        try:
            return self.channel.exchange_unbind(destination=destination, source=source,
                                                routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def publish(self, exchange_name, routing_key, body, properties=None, mandatory=False):
        while True:
            try:
                self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key,
                                           body=body, properties=properties,
                                           mandatory=mandatory)
                break
            except:
                self.reconfig()

    def consume(self, queue_name, on_consume_callback, reconnect=False):
        try:
            if not reconnect:
                self.consume_info[queue_name] = on_consume_callback
            self.channel.basic_consume(queue=queue_name, on_message_callback=on_consume_callback)

        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def start_consuming(self):
        while True:
            try:
                #self.channel.basic_qos(prefetch_count=1)
                self.channel.start_consuming()
                break
            except:
                self.reconfig()

                for queue_name in self.consume_info:
                    self.consume(queue_name, self.consume_info[queue_name],reconnect=True)

    def stop_consuming(self):
        try:
            self.channel.stop_consuming()
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err.args)

    def reconfig(self):
        if self.open(user=self.__user,
                     password=self.__password,
                     host=self.__host,
                     port=self.__port,
                     virtual_host=self.__virtual_host) is None:
            time.sleep(1)
