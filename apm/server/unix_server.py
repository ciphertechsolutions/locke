import socket
import os

from apm.server import SocketServer, SocketServerThread


class UnixServer(SocketServer):
    """docstring for UnixServer"""
    def __init__(self, file='/tmp/apm.sock'):
        super().__init__()
        self.file = file

    def start(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.file)
        self.sock.listen(5)

        while True:
            client, _ = self.sock.accept()
            SocketServerThread(client).start()

    def stop(self):
        super()
        os.remove(self.file)


if __name__ == '__main__':
    import click
    import patterns

    @click.command()
    @click.option('--socket', default='/tmp/apm.sock', help='The UNIX socket')
    def cli(socket):
        server = UnixServer(file=socket)
        server.start()

    cli()
