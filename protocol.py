from autobahn.twisted.websocket import WebSocketServerProtocol


class BroadcastServerProtocol(WebSocketServerProtocol):

    def onOpen(self):
        self.username = None
        self.factory.register(self)
        self.factory.broadcastChatUsers()
        self.sendChat()

    def onMessage(self, payload, isBinary):
        if not isBinary:
            msg = payload.decode('utf8')
            if msg.startswith('/name'):
                self.setUsername(msg.split(' ', 1)[-1])
                print 'Client username set to "{}"'.format(self)
            else:
                self.factory.broadcast(self, msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)
        self.factory.broadcastChatUsers()

    def sendEntry(self, entry):
        msg = '[{}] {}: {}'.format(
            entry.timestamp.isoformat(),
            entry.sender,
            entry.msg
        )
        self.sendMessage(msg)
        print 'Message "{}" sent to {}'.format(msg, self)

    def sendChat(self):
        for entry in self.factory.chat:
            self.sendEntry(entry)

    def sendChatUsers(self):
        msg = '/users {}'.format(
            ','.join(
                [str(user) for user in self.factory.users]
            )
        )
        self.sendMessage(msg)

    def setUsername(self, username):
        self.username = username
        print 'Client username set to "{}"'.format(self)
        self.factory.broadcastChatUsers()

    def __str__(self):
        return self.username or self.peer
