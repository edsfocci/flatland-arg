#!/usr/bin/env python
# Copyright (c) 2009-2010 Twisted Matrix Laboratories.
# See LICENSE for details.

from game.controller import TrackerController
from twisted.spread import pb
from twisted.internet import defer
from twisted.internet import reactor
from twisted.cred import credentials
from twisted.internet.protocol import DatagramProtocol


class Bootstrap(DatagramProtocol):
    def datagramReceived(self, datagram, address):
        if datagram == "FlatlandARG!!!":
            self.port.stopListening()
            ip, port = address
            Tracker().connect(ip)
            

class Tracker():
    def connect(self, ip):
        factory = pb.PBClientFactory()
        reactor.connectTCP(ip, 8800, factory)
        d = factory.login(credentials.Anonymous())
        d.addCallback(self.connected)

    @defer.inlineCallbacks
    def connected(self, perspective):
        self.perspective = perspective
        self.environment = yield perspective.callRemote('getEnvironment')
        self.environment.team = yield perspective.callRemote('getTeam')
        self.view.start("Client - %d" % (self.environment.team, ))
        self.controller = TrackerController(self.perspective, self.view)
        self.controller.go()

    def shutdown(self, result):
        reactor.stop()


bootstrap = Bootstrap()
bootstrap.port = reactor.listenUDP(8000, bootstrap)
reactor.run()
