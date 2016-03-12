from abc import ABCMeta, abstractmethod
from circuits import Component, Event
from os import getpid

from trading.emitter.component import Component, listen_on

class Strategy(Component):
  __metaclass__ = ABCMeta

  @abstractmethod
  def calculate_signals(self):
    raise NotImplementedError("Should implement calculate_signals()")

class CandleBuilder(Component):

  def started(self, *args):
    print("CandleBuilder started [{}]".format(getpid()))

  @listen_on('tick')
  def t(self, *event):
    print("Received tick")
