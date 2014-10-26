#!/usr/bin/env python

__author__ = 'me@billdimmick.com'

from os import path
from time import strftime
from twisted.internet import reactor, protocol

# TODO(bfd): Add a way to pass command-line arguments for drop directory, max bytes, and port

DESTDIR = '/tmp'

class DeaddropProtocol(protocol.Protocol):
  def __init__(self):
    self.destination = None

  def filename(self):
    return "%s@%s" % (self.transport.getPeer().host, strftime("%Y%m%d%H%M%S"))

  def connectionMade(self):
    self.destination = open(path.join(DESTDIR, self.filename()), "w")

  def dataReceived(self, data):
    self.destination.write(data)

  def connectionLost(self, reason):
    self.destination.close()


def main():
  factory = protocol.ServerFactory()
  factory.protocol = DeaddropProtocol
  reactor.listenTCP(4233, factory)
  reactor.run()


if __name__ == '__main__':
  main()
