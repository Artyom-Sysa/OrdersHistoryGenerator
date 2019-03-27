import abc


class FileService(abc.ABC):
    @abc.abstractmethod
    def read_all(self, *args, **kwargs):
        pass
    @abc.abstractmethod
    def write(self, data, mode, *args, **kwargs):
        pass
