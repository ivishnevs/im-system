# -*- coding: utf-8 -*-

import models as m


class BaseHandler(object):
    def __init__(self, me, recipients=None, server=None, ):
        self.me = me
        self.server = server
        self.recipients = recipients # must foo

    def handle(self, msg):
        self.me.push("Enter the command, please!\n")


class RegHandler(BaseHandler):

    def handle(self, msg):
        if msg:
            if self.me.username:
                user = m.User(self.me.username, msg, "")
                m.session.add(user)
                m.session.commit()
                self.me.push(self.me.username+" is created!\n")
                self.server.users_map[self.me.username] = self.me
                self.me.push("Waiting for the next command...\n")
                self.me.handler = BaseHandler(self.me)
            else:
                user = m.session.query(m.User).filter_by(name=msg).first()
                if user:
                    self.me.push("This user is exist.\n")
                else:
                    self.me.username = msg
                    self.me.push("Enter your password...\n")
        else:
            self.me.push("Enter new login...\n")


class AuthHandler(BaseHandler):

    def handle(self, msg):
        if msg:
            if self.me.username:
                user = m.session.query(m.User).filter_by(name=self.me.username).first()
                if user.password == msg:
                    self.me.push("Done!\n")
                    self.server.users_map[self.me.username] = self.me
                    self.me.push("Waiting for the next command...\n")
                    self.me.handler = BaseHandler(self.me)
                else:
                    self.me.push("Incorrect password. Enter another, please...\n")
            else:
                user = m.session.query(m.User).filter_by(name=msg).first()
                if user:
                    self.me.username = msg
                    self.me.push("Enter your password...\n")
                else:
                    self.me.push("The user isn't found. Enter another login...\n")

        else:
            if self.me.username:
                del self.server.users_map[self.me.username]
                self.me.username = ''
            self.me.push("Enter your login...\n")


class ChatHandler(BaseHandler):

    def handle(self, msg):
        if msg:
            for recipient in self.recipients.values():
                recipient.push(self.me.prompt+msg+"\n")
