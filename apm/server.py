import socket
import struct
from threading import Thread

import msgpack

import apm


class ServerThread(Thread):
    """docstring for ServerThread"""
    def __init__(self, client):
        super(ServerThread, self).__init__()
        self.client = client

    def run(self):
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


class Server(object):
    """docstring for Server"""
    def __init__(self, host='localhost', port=1337):
        super(Server, self).__init__()
        self.host = host
        self.port = port
        self.sock = None

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        while True:
            client, _ = self.sock.accept()
            ServerThread(client).start()

    def stop(self):
        self.sock.close()
        self.sock = None


if __name__ == '__main__':
    import click
    import patterns

    @click.command()
    @click.option('--host', default='localhost', help='The host to bind to')
    @click.option('--port', default=1337, help='The port to listen on')
    def cli(host, port):
        server = Server(host=host, port=port)
        server.start()

    cli()
