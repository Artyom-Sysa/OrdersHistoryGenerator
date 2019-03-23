import abc


class PseudorandomNumberGenerator(abc.ABC):

    @abc.abstractmethod
    def get_next(self, **kwargs):
        pass

    @abc.abstractmethod
    def set_seed(self, **kwargs):
        pass
