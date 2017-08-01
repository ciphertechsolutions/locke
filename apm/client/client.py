from abc import ABC, abstractmethod


class Client(ABC):
    """docstring for Client"""
    def __init__(self, stage=1):
        super().__init__()
        self.stage = stage

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def send_data(self, data):
        pass

    def send_file(self, file):
        with open(file, 'rb') as f:
            data = f.read()

        self.send_data(data)
