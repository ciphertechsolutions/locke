import socket

from apm.client import SocketClient


class TCPClient(SocketClient):
    """
    A TCP client that issues requests understood by the TCPServer class.
    """
    def __init__(self, host: str = 'localhost', port: int = 1337,
                 stage: int = 1):
        super().__init__(stage=stage)
        self.host = host
        self.port = port

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))


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
