from abc import ABC, abstractmethod

class Server(ABC):
    """docstring for Server"""
    def __init__(self):
        super(Server, self).__init__()

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
