from autobahn.twisted.websocket import listenWS
from twisted.internet import reactor

from factory import BroadcastServerFactory
from protocol import BroadcastServerProtocol


if __name__ == '__main__':
    factory = BroadcastServerFactory('ws://0.0.0.0:9000')
    factory.protocol = BroadcastServerProtocol
    listenWS(factory)
    reactor.run()
