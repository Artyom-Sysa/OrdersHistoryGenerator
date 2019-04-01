import abc


class PseudorandomNumberGenerator(abc.ABC):

    @abc.abstractmethod
    def get_next(self, **kwargs):
        '''
        Generate next value of generator
        '''
        pass

    @abc.abstractmethod
    def set_seed(self, **kwargs):
        '''
        Set parameters to generator
        '''
        pass
