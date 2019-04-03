import abc


class FileService(abc.ABC):
    @abc.abstractmethod
    def read(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def write(self, data, mode, *args, **kwargs):
        pass
