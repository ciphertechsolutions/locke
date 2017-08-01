from apm.server.tcp_server import TCPServer

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
