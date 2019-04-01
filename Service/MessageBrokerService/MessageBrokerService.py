import abc


class MessabeBrokerService(abc.ABC):
    @abc.abstractmethod
    def open_connection(self, host=None, port=None, user=None, password=None, *args, **kwargs):
        pass

    @abc.abstractmethod
    def close(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def publish(self, *args, **kwargs):
        pass
