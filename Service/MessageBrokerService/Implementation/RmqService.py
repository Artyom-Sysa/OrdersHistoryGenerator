from Service.MessageBrokerService.MessageBrokerService import MessabeBrokerService
from Service.AbstractConnection.Implementation.RmqConnection import RmqConnection
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
import pika


class RmqService(MessabeBrokerService):
    def __init__(self):
        self.conn = None

    def open_connection(self, user=pika.connection.Parameters.DEFAULT_USERNAME,
                        password=pika.connection.Parameters.DEFAULT_PASSWORD,
                        host=pika.connection.Parameters.DEFAULT_HOST,
                        port=pika.connection.Parameters.DEFAULT_PORT, *args, **kwargs):
        '''
        Opening RMQ connection

        :param user: username
        :param password: password
        :param host: host
        :param port: port
        :param args:
        :param kwargs: must containts virtual_host
        :return:
        '''
        Logger.debug(__file__, 'Opening RMQ connection')
        self.conn = RmqConnection()

        if 'virtual_host' in kwargs:
            virtual_host = kwargs['virtual_host']
        else:
            virtual_host = pika.connection.Parameters.DEFAULT_VIRTUAL_HOST

        self.conn.open(host=host, port=port, user=user, password=password, virtual_host=virtual_host)

        return self.conn.is_available()

    def close(self, *args, **kwargs):
        ''''
        Closing RMQ service
        '''
        Logger.debug(__file__, 'Closing RMQ connection')
        self.conn.close()

    def publish(self, exchange_name, routing_key, body, properties=None, mandatory=False, *args, **kwargs):
        '''
        Sending body to exchange with routing key

        :param exchange_name: exchange name
        :param routing_key: routing key
        :param body: message body
        :param properties:
        :param mandatory:
        :param channel_number:
        :param args:
        :param kwargs:
        :return:
        '''

        self.conn.publish(exchange_name, routing_key, body, properties=properties, mandatory=mandatory)

    def declare_exchange(self, exchange_name, exchange_type, passive=False, durable=True, auto_delete=False):
        '''
        Declare new exchange

        :param exchange_name: exchange name
        :param exchange_type: exhange type
        :param passive:
        :param durable:
        :param auto_delete:
        :return:
        '''

        Logger.debug(__file__, 'Declaring exchange {} with exchange type'.format(exchange_name, exchange_type.value))

        return self.conn.declare_exchange(exchange_name,
                                          exchange_type,
                                          passive=passive,
                                          durable=durable,
                                          auto_delete=auto_delete
                                          )

    def declare_queue(self, queue_name):
        '''
        Declare new queue

        :param queue_name: queue name
        :return:
        '''

        Logger.debug(__file__, 'Declaring queue with name {}'.format(queue_name))
        return self.conn.declare_queue(queue_name=queue_name)

    def queue_bind(self, queue_name, exchange_name, routing_key=None):
        '''
        Binding queue to exchange

        :param queue_name: queue name
        :param exchange_name: exchange name
        :param routing_key: routing key
        :return:
        '''

        Logger.debug(__file__, 'Binding queue {} to exchange {} with routing key  {}'.format(queue_name, exchange_name,
                                                                                             routing_key))

        return self.conn.queue_bind(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)

    def queue_unbind(self, queue_name, exchange_name, routing_key=None):
        Logger.debug(__file__,
                     'Unbinding queue {} from exchange {} with routing key  {}'.format(queue_name, exchange_name,
                                                                                       routing_key))
        return self.conn.queue_unbind(queue_name=queue_name, exchange_name=exchange_name, routing_key=routing_key)

    def queue_purge(self, queue_name):
        '''
        Clearing queue

        :param queue_name: queue name
        :return:
        '''

        Logger.debug(__file__, 'Purging queue {}'.format(queue_name))
        return self.conn.queue_purge(queue_name)

    def queue_delete(self, queue_name, if_unused=False, if_empty=False):
        Logger.debug(__file__, 'Deleting queue {}'.format(queue_name))
        return self.conn.queue_delete(queue_name, if_unused=if_unused, if_empty=if_empty)

    def exchange_delete(self, exchange_name=None, if_unused=False):
        '''
        Delete exchange

        :param exchange_name: exchange name
        :param if_unused:
        :return:
        '''

        Logger.debug(__file__, 'Deleting exchange {}'.format(exchange_name))
        return self.conn.exchange_delete(exchange_name=exchange_name, if_unused=if_unused)

    def exchange_bind(self, destination, source, routing_key=''):
        '''
        Bind exchange
        '''

        Logger.debug(__file__,
                     'Bind exchange: destination {}, sourse, routing_key'.format(destination, source, routing_key))
        return self.conn.exchange_bind(destination=destination, source=source, routing_key=routing_key)

    def exchange_unbind(self, destination, source, routing_key=''):
        '''
        Unind exchange
        '''

        Logger.debug(__file__,
                     'Unbind exchange: destination {}, sourse, routing_key'.format(destination, source, routing_key))
        return self.conn.exchange_unbind(destination=destination, source=source, routing_key=routing_key)

    def consume(self, queue_name, on_consume_callback):
        self.conn.consume(queue_name=queue_name, on_consume_callback=on_consume_callback)

    def start_consuming(self):
        return self.conn.start_consuming()
