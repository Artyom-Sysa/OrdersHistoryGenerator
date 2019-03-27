import abc


class AbstractConnection(abc.ABC):
    @abc.abstractmethod
    def open(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def close(self, *args, **kwargs):
        pass
    
    @abc.abstractmethod
    def is_available(self):
        pass
