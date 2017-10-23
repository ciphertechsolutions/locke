import os
import socket

from apm.server import SocketServer, SocketServerThread


class UnixServer(SocketServer):
    """
    A Unix domain socket server that listens for requests,
    processes the data within those requests, and sends the
    results as msgpack-formatted lists and dictionaries.
    """

    def __init__(self, file: str = '/tmp/apm.sock'):
        super().__init__()
        self.file = file

    def start(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(self.file)
        self.sock.listen(5)

        while True:
            client, _ = self.sock.accept()
            SocketServerThread(client).start()

    def stop(self) -> None:
        super()
        os.remove(self.file)


if __name__ == '__main__':
    import click


    @click.command()
    @click.option('--socket', default='/tmp/apm.sock', help='The UNIX socket')
    def cli(socket):
        server = UnixServer(file=socket)
        server.start()


    cli()
