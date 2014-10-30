#!/usr/bin/env python

__author__ = 'me@billdimmick.com'

from argparse import ArgumentParser
from os import path
from time import strftime
from twisted.internet import reactor, protocol

# TODO(bfd): Add a way to pass command-line arguments for drop directory, max bytes, and port

class DeaddropProtocol(protocol.Protocol):
  def __init__(self):
    self.destination = None

  def filename(self):
    return "%s@%s" % (self.transport.getPeer().host, strftime("%Y%m%d%H%M%S"))

  def connectionMade(self):
    self.destination = open(path.join(self.factory.root, self.filename()), "w")

  def dataReceived(self, data):
    self.destination.write(data)

  def connectionLost(self, reason):
    self.destination.close()


class DeaddropFactory(protocol.ServerFactory):
  protocol = DeaddropProtocol

  def __init__(self, root):
    self.root = root


def start(port=4233, root='/tmp', debug=False):
  reactor.listenTCP(port, DeaddropFactory(root))
  reactor.run()

def parse_args():
  parser = ArgumentParser(description = 'Starts a deaddrop server on this host.')
  parser.add_argument('--port', dest='port', action='store', default=4233, type=int)
  parser.add_argument('--root', dest='root', action='store', default='/tmp')
  parser.add_argument('--debug', dest='debug', action='store_true', default=False)
  return parser.parse_args()


if __name__ == '__main__':
  args = parse_args()
  start(args.port, args.root, args.debug)
