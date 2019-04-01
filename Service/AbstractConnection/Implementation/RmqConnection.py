import pika

from Service.AbstractConnection.AbstractConnection import AbstractConnection
from pika import exceptions
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger


class RmqConnection(AbstractConnection):
    def __init__(self):
        self.connection = None
        self.channel = None

    def open(self, user=pika.connection.Parameters.DEFAULT_USERNAME,
             password=pika.connection.Parameters.DEFAULT_PASSWORD,
             host=pika.connection.Parameters.DEFAULT_PORT,
             port=pika.connection.Parameters.DEFAULT_PORT,
             virtual_host=pika.connection.Parameters.DEFAULT_VIRTUAL_HOST):
        try:
            credentials = pika.PlainCredentials(username=user, password=password)
            params = pika.ConnectionParameters(host=host, port=port, virtual_host=virtual_host, credentials=credentials)

            self.connection = pika.BlockingConnection(params)
            self.channel = self.connection.channel()
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def close(self, *args, **kwargs):
        try:
            if self.connection.is_open:
                self.close()
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def is_available(self):
        return self.connection.is_open

    def declare_exchange(self, exchange_name,
                         exchange_type,
                         passive=False,
                         durable=True,
                         auto_delete=False):
        try:
            return self.channel.exchange_declare(exchange=exchange_name,
                                                 exchange_type=exchange_type.value,
                                                 passive=passive,
                                                 durable=durable,
                                                 auto_delete=auto_delete)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def declare_queue(self, queue_name):
        try:
            return self.channel.queue_declare(queue=queue_name)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def queue_bind(self, queue_name, exchange_name, routing_key=None):
        try:
            return self.channel.queue_bind(queue_name, exchange_name, routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def queue_unbind(self, queue_name, exchange_name, routing_key=None):
        try:
            return self.channel.queue_unbind(queue_name, exchange_name, routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def queue_purge(self, queue_name):
        try:
            return self.channel.queue_purge(queue_name)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def queue_delete(self, queue_name, if_unused=False, if_empty=False):
        try:
            return self.channel.queue_delete(queue_name, if_unused=if_unused, if_empty=if_empty)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def exchange_delete(self, exchange_name=None, if_unused=False):
        try:
            return self.channel.exchange_delete(exchange=exchange_name, if_unused=if_unused)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def exchange_bind(self, destination, source, routing_key=''):
        try:
            return self.channel.exchange_bind(destination=destination, source=source,
                                              routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def exchange_unbind(self, destination, source, routing_key=''):
        try:
            return self.channel.exchange_unbind(destination=destination, source=source,
                                                routing_key=routing_key)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def publish(self, exchange_name, routing_key, body, properties=None, mandatory=False):
        try:
            self.channel.basic_publish(exchange=exchange_name, routing_key=routing_key,
                                       body=body, properties=properties,
                                       mandatory=mandatory)

        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def consume(self, queue_name, on_consume_callback):
        try:
            self.channel.basic_consume(queue_name, on_consume_callback)
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)

    def start_consuming(self):
        try:
            self.channel.start_consuming()
        except pika.exceptions.AMQPError as err:
            Logger.error(__file__, err)
            print(err)
