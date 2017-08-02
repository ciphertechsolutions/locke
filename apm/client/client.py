from abc import ABC, abstractmethod
import struct

import msgpack


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


class SocketClient(Client):
    """
    A superclass client for all APM client interfaces that use socket objects.

    The protocol spoken by APM socket clients is very simple, with an 8-byte
    header followed by N bytes of data:
        <nbytes><stage><data>

    <nbytes> is a 4-byte network (big-endian) word, specifying the size
    of <data>.

    <stage> is a 4-byte network (big-endian) word, specifying the "stage"
    of the patterns that the client expects to be run.

    <data> is <nbytes> of binary data, fed directly into the pattern matching
    core. No packing or unpacking is done to this data.

    For example, this would be a valid transmission requesting the analysis
    of 4 bytes of data via stage 1:
        b'\x00\x00\x00\x04\x00\x00\x00\x01asdf'
    """
    def __init__(self, stage=1):
        super().__init__(stage=stage)
        self.sock = None

    def disconnect(self) -> None:
        self.sock.close()

    def send_data(self, data: bytes) -> None:
        handshake = struct.pack('>2I', len(data), self.stage)
        self.sock.send(handshake)
        self.sock.sendall(data)

        unpacker = msgpack.Unpacker()
        buf = self.sock.recv(4096)
        while buf:
            unpacker.feed(buf)
            buf = self.sock.recv(4096)
            for unpacked in unpacker:
                yield unpacked
