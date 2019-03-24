import abc


class ConfigLoader(abc.ABC):
    @abc.abstractmethod
    def load(self, *args, **kwargs):
        '''
        Load configuration to Configuration object from local or remote source
        '''
        pass

    @abc.abstractmethod
    def write_default(self, *args, **kwargs):
        '''
        Write default settings to local or remove default configuration source
        '''
        pass
