from abc import ABC, abstractmethod
from threading import Thread
import struct
import socket

import msgpack

import apm


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


class SocketServer(Server):
    """
    A superclass server for all APM server instances that use socket objects.
    """
    def __init__(self):
        super().__init__()
        self.sock = None

    def stop(self) -> None:
        self.sock.close()
        self.sock = None


class SocketServerThread(Thread):
    """
    An individual server thread for the TCP server.
    """
    def __init__(self, client: socket.socket):
        super().__init__()
        self.client = client

    def run(self) -> None:
        handshake = self.client.recv(8)
        if not handshake or len(handshake) < 8:
            return None

        size, stage = struct.unpack('>2I', handshake)

        if stage < 1:
            stage = 1

        buf = self.client.recv(size)
        while len(buf) < size:
            buf += self.client.recv(size)

        mgr = apm.Manager(raw=buf, stage=stage)
        for pat, matches in mgr.run():
            if not matches:
                continue

            match_hash = {}
            for match in matches:
                match_hash[match.offset] = match.data

            msg = msgpack.packb([pat.Description, pat.Weight, match_hash])
            self.client.sendall(msg)
        del mgr
        self.client.close()
