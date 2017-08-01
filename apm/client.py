from apm.client.tcp_client import TCPClient

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
