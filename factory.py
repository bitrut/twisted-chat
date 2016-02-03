from collections import namedtuple
from datetime import datetime

from autobahn.twisted.websocket import WebSocketServerFactory


Entry = namedtuple('Entry', ['timestamp', 'sender', 'message'])


class BroadcastServerFactory(WebSocketServerFactory):
    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        super(BroadcastServerFactory, self).__init__(
            url, debug=debug, debugCodePaths=debugCodePaths
        )
        self.users = []
        self.chat = []

    def register(self, user):
        if user not in self.users:
            print "Registered user {}".format(user)
            self.users.append(user)

    def unregister(self, user):
        if user in self.users:
            print "Unregistered user {}".format(user)
            self.users.remove(user)

    def broadcast(self, sender, message):
        print "Broadcasting message '{}' from {}".format(
            message.encode('utf8'), sender
        )
        entry = Entry(timestamp=datetime.now(), sender=sender, message=message)
        for user in self.users:
            user.sendEntry(entry)
        self.chat.append(entry)

    def broadcastChatUsers(self):
        for user in self.users:
            user.sendChatUsers()
