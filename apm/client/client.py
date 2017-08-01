from abc import ABC, abstractmethod


class Client(ABC):
    """
    An abstract Client for APM interfaces to subclass.
    """
    def __init__(self, stage: int = 1):
        super().__init__()
        self.stage = stage

    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def send_data(self, data: bytes) -> None:
        pass

    def send_file(self, file: str) -> None:
        with open(file, 'rb') as f:
            data = f.read()

        self.send_data(data)
