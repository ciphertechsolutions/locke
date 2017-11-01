import socket

from apm.server import SocketServer, SocketServerThread


class TCPServer(SocketServer):
    """
    A TCP server that listens for requests, processes the data
    within those requests, and sends the results as msgpack-formatted
    lists and dictionaries.
    """

    def __init__(self, host: str = 'localhost', port: int = 1337):
        super().__init__()
        self.host = host
        self.port = port

    def start(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

        while True:
            client, _ = self.sock.accept()
            SocketServerThread(client).start()


if __name__ == '__main__':
    import click


    @click.command()
    @click.option('--host', default='localhost', help='The host to bind to')
    @click.option('--port', default=1337, help='The port to listen on')
    def cli(host, port):
        server = TCPServer(host=host, port=port)
        server.start()


    cli()
