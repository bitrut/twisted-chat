import json

from autobahn.twisted.websocket import WebSocketServerProtocol


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.username = None
        self.factory.register(self)
        self.factory.broadcastChatUsers()
        self.sendChat()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            message = payload.decode('utf8')
            if message.startswith('/username'):
                self.setUsername(message.split(' ', 1)[-1])
                print 'Client username set to "{}"'.format(self)
            else:
                self.factory.broadcast(self, message)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
        self.factory.broadcastChatUsers()

    def sendEntry(self, entry):
        message = json.dumps({
            'timestamp': entry.timestamp.isoformat(),
            'sender': str(entry.sender),
            'message': entry.message
        })
        self.sendMessage(message)
        print 'Message "{}" sent to {}'.format(message, self)

    def sendChat(self):
        for entry in self.factory.chat:
            self.sendEntry(entry)

    def sendChatUsers(self):
        message = '/users {}'.format(
            ','.join(
                [str(user) for user in self.factory.users]
            )
        )
        self.sendMessage(message)

    def setUsername(self, username):
        self.username = username
        print 'Client username set to "{}"'.format(self)
        self.factory.broadcastChatUsers()

    def __str__(self):
        return self.username or self.peer
