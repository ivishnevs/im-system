# -*- coding: utf-8 -*-

import asyncore
import socket
import sys
import asynchat


class Client(asynchat.async_chat):
    def __init__(self, addr):
        asynchat.async_chat.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect(addr)

        self.set_terminator('\n')
        self.buffer = []

    def handle_connect(self):
        print("Connected. Type \help for more information...\n")

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def found_terminator(self):
        msg = ''.join(self.buffer)
        print ('\033[92m    '+ msg+ '\033[0m')
        self.buffer = []


class ConsoleLineClient(asyncore.file_dispatcher):
    def __init__(self, client, file):
        asyncore.file_dispatcher.__init__(self, file)
        self.client = client

    def handle_read(self):
        self.client.push(self.recv(1024))

import config
addr = (config.SERVER_HOST, config.SERVER_PORT)

client = Client(addr)
consoleline = ConsoleLineClient(client, sys.stdin)
asyncore.loop()
