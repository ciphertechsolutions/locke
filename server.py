#!/usr/bin/env python3

# system modules
import socket
import struct
from threading import Thread

# external modules
import click
import msgpack

# apm modules
import apm
import patterns


def client_handler(client):
    size = client.recv(4)

    if not size or len(size) < 4:
        return None

    size = struct.unpack('>I', size)[0]

    buf = client.recv(size)
    while len(buf) < size:
        buf += client.recv(size)

    mgr = apm.Manager(raw=buf)
    for pat, matches in mgr.run():
        if not matches:
            continue

        match_hash = {}
        for match in matches:
            match_hash[match.offset] = match.data

        msg = msgpack.packb([pat.Description, match_hash])
        client.sendall(msg)
    client.close()


@click.command()
@click.option('--host', default='localhost', help='The host to bind to')
@click.option('--port', default=1337, help='The port to listen on')
def cli(host, port):
    """
    Start a new APM server instance, listening on the given host and port.
    """
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((host, port))
    serv.listen(5)  # XXX: Is this a reasonable default?

    while True:
        client, _ = serv.accept()
        Thread(target=client_handler, args=(client,)).start()


if __name__ == '__main__':
    cli()
