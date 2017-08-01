import socket
import struct

from apm.client import Client

import msgpack


class TCPClient(Client):
    """
    A TCP client that issues requests understood by the TCPServer class.

    The protocol spoken by APM TCP clients is very simple, with an 8-byte
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
    def __init__(self, host: str = 'localhost', port: int = 1337,
                 stage: int = 1):
        super().__init__(stage=stage)
        self.host = host
        self.port = port
        self.sock = None

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def disconnect(self) -> None:
        self.sock.close()
        self.sock = None

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

    def send_file(self, file: str) -> None:
        with open(file, 'rb') as f:
            data = f.read()

        return self.send_data(data)


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('--host', default='localhost', help='The host to connect to')
    @click.option('--port', default=1337, help='The port to connect on')
    @click.option('--stage', default=1, help='The processing stage')
    @click.argument('file', type=click.File('rb'), nargs=1)
    def cli(host, port, stage, file):
        client = TCPClient(host=host, port=port, stage=stage)
        client.connect()

        for obj in client.send_data(file.read()):
            print(obj)

        client.disconnect()

    cli()
