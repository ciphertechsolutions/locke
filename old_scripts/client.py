#!/usr/bin/env python3

# system modules
import socket
import struct

# external modules
import click
import msgpack


@click.command()
@click.option('--host', default='localhost', help='The host to connect to')
@click.option('--port', default=1337, help='The port to connect on')
@click.argument('file', type=click.File('rb'), nargs=1)
def cli(host, port, file):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    data = file.read()
    size = len(data)
    size_msg = struct.pack('>I', size)
    unpacker = msgpack.Unpacker()

    sock.send(size_msg)
    sock.sendall(data)

    data = None  # no need to keep this hanging around

    while True:
        buf = sock.recv(4096)

        if not buf:
            break

        unpacker.feed(buf)

        for unpacked in unpacker:
            print(unpacked)

    sock.close()


if __name__ == '__main__':
    cli()
