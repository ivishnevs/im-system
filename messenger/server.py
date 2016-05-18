# -*- coding: utf-8 -*-

import re
import asynchat
import asyncore
import socket
import config
from handlers import BaseHandler, AuthHandler, RegHandler, ChatHandler


class MainHandler(asynchat.async_chat):
    def __init__(self, sock, server):
        asynchat.async_chat.__init__(self, sock=sock, map=server.sock_map)
        self.set_terminator('\n')
        self.prompt = ''
        self.recipients = {}
        self.username = ''
        self.server = server
        self.buffer = []
        self.handler = BaseHandler(self)

    def collect_incoming_data(self, data):
        self.buffer.append(data)

    def get_handler(self, request):
        if re.match(r'^\\auth$', request):  # handle auth
            return AuthHandler(me=self, server=self.server), ''

        elif re.match(r'^\\reg$', request):
            return RegHandler(me=self, server=self.server), ''

        elif re.match(r'^\\chatwith', request):  # handle chat
            if self.username:
                request = request.replace('\chatwith', '')
                recipients_names = request.split(' ')

                self.prompt = '[%s@%s]>' % (self.username, self.addr[0])
                for name in recipients_names:
                    if name:
                        if name in server.users_map.iterkeys():
                            self.recipients[name] = server.users_map[name]
                        else:
                            self.push(name + " is offline!\n")

                if self.recipients:
                    return ChatHandler(me=self, recipients=self.recipients), 'Connected.'

            else:
                self.push("You need to authorize...\n")

        elif re.match(r'^\\online$', request):
            names = ''
            if server.users_map:
                for name in server.users_map.keys():
                    names += name + ', '
            self.push("Now online: " + names + "\n")
            return self.handler, ''

        elif re.match(r'^\\help$', request):
            self.push("There are some commands for manage this messenger:\n")
            self.push("Type \\reg for registration \n")
            self.push("\\auth for authorize \n")
            self.push("\\online to check which users online\n")
            self.push("\\chatwith username1 [username2] [... \n")
            self.push("\n")
            return self.handler, ''

        else:
            return self.handler, request

    def found_terminator(self):
        request = ''.join(self.buffer)
        self.handler, msg = self.get_handler(request)
        self.handler.handle(msg)
        self.buffer = []

    def handle_close(self):
        if self.username in self.server.users_map.keys():
            del self.server.users_map[self.username]
        self.buffer.append("Disconected.\n")
        self.found_terminator()
        print '%s:%s disconected' % self.addr
        self.close()


class ChatServer(asyncore.dispatcher):
    sock_map = {}
    users_map = {}  # {username: asynchat instance), }

    def __init__(self, addr):
        asyncore.dispatcher.__init__(self, map=self.sock_map)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.bind(addr)
        self.listen(config.BACKLOG)

    def handle_accept(self):
        (sock, client_address) = self.accept()
        print 'Incoming connection from %s:%s' % client_address
        # todo check ip
        handler = MainHandler(sock, self)


addr = (config.SERVER_HOST, config.SERVER_PORT)
server = ChatServer(addr)

print 'Server run on %s:%s' % addr
asyncore.loop(map=server.sock_map)
