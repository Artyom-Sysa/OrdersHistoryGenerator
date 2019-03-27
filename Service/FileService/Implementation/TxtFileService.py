from Service.AbstractConnection.Implementation.FileDescriptor import FileDescriptor
from Service.FileService.FileService import FileService


class TxtFileService(FileService):
    def __init__(self, path):
        self.__file_descriptor = FileDescriptor(path)
        self.path = path

    def read_all(self, *args, **kwargs):
        pass

    def write(self, data, mode, *args, **kwargs):
        if self.__file_descriptor.mode != mode:
            self.__file_descriptor.close()
            self.__file_descriptor.open(path=self.path, mode=mode)

        self.__file_descriptor.write(data)

    def close(self):
        self.__file_descriptor.close()

