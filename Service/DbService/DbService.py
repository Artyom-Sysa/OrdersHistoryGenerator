import abc


class DbService(abc.ABC):
    @abc.abstractmethod
    def execute(self, query, *args, **kwargs):
        pass
