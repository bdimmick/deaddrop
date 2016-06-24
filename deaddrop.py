#!/usr/bin/env python

__author__ = 'me@billdimmick.com'

from argparse import ArgumentParser
from os import path
from string import digits
from time import strftime
from twisted.internet import reactor, protocol

class DeaddropProtocol(protocol.Protocol):
  def __init__(self):
    self.destination = None
    self.count = 0

  def connectionMade(self):
    filename = "%s@%s" % (self.transport.getPeer().host, strftime("%Y%m%d%H%M%S"))
    self.destination = open(path.join(self.factory.root, filename), "w")

  def dataReceived(self, data):
    self.destination.write(data)
    self.count += len(data)
    if self.count > self.factory.maxlen:
      self.transport.loseConnection()

  def connectionLost(self, reason):
    self.destination.close()


class DeaddropFactory(protocol.ServerFactory):
  protocol = DeaddropProtocol

  def __init__(self, root, maxlen):
    self.root = root
    self.maxlen = maxlen


SIZES = {
  'K': 1024,
  'M': 1024 * 1024,
  'G': 1024 * 1024 * 1024
}


def byteLength(value):
  if not value:
    return 0

  suffix = value[-1:].upper()
  try:
    if suffix in digits:
      return int(value)
    if suffix in SIZES:
      return SIZES[suffix] * int(value[:-1])
  except ValueError:
    pass
  raise ValueError("Provided value '%s' is not a value size in bytes." % value)


def start(port=4233, root='/tmp', debug=False, maxlen='1M'):
  reactor.listenTCP(port, DeaddropFactory(root, byteLength(maxlen)))
  reactor.run()


def parse_args():
  parser = ArgumentParser(description = 'Starts a deaddrop server on this host.')
  parser.add_argument('--port', dest='port', action='store', default=4233, type=int)
  parser.add_argument('--maxlen', dest='maxlen', action='store', default='1M', type=str)
  parser.add_argument('--root', dest='root', action='store', default='/tmp')
  parser.add_argument('--debug', dest='debug', action='store_true', default=False)
  return parser.parse_args()


if __name__ == '__main__':
  args = parse_args()
  start(port=args.port, root=args.root, debug=args.debug, maxlen=args.maxlen)
