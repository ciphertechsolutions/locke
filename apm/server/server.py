from abc import ABC, abstractmethod

class Server(ABC):
    """
    An abstract Server for APM interfaces to subclass.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass
