import socket

from apm.client import SocketClient


class UnixClient(SocketClient):
    """
    A Unix domain socket client that issues requests understood
    by the UnixServer class.
    """
    def __init__(self, file='/tmp/apm.sock', stage=1):
        super().__init__(stage=stage)
        self.file = file
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.connect(self.file)


if __name__ == '__main__':
    import click

    @click.command()
    @click.option('--socket', default='/tmp/apm.sock', help='The UNIX socket')
    @click.option('--stage', default=1, help='The processing stage')
    @click.argument('file', type=click.File('rb'), nargs=1)
    def cli(socket, stage, file):
        client = UnixClient(file=socket, stage=stage)
        client.connect()

        for obj in client.send_data(file.read()):
            print(obj)

        client.disconnect()

    cli()
