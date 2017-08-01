import socket
import struct
from threading import Thread

import msgpack

import apm
from apm.server import Server


class TCPServerThread(Thread):
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
        self.client.close()


class TCPServer(Server):
    """
    A TCP server that listens for requests, processes the data
    within those requests, and returns the results as msgpack-formatted
    lists and dictionaries.
    """
    def __init__(self, host: str = 'localhost', port: int = 1337):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = None

    def start(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        while True:
            client, _ = self.sock.accept()
            TCPServerThread(client).start()

    def stop(self) -> None:
        self.sock.close()
        self.sock = None


if __name__ == '__main__':
    import click
    import patterns

    @click.command()
    @click.option('--host', default='localhost', help='The host to bind to')
    @click.option('--port', default=1337, help='The port to listen on')
    def cli(host, port):
        server = TCPServer(host=host, port=port)
        server.start()

    cli()
