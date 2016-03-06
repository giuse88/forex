from abc import ABCMeta, abstractmethod
from circuits import Component

class Strategy(Component):
  __metaclass__ = ABCMeta

  @abstractmethod
  def calculate_signals(self):
    raise NotImplementedError("Should implement calculate_signals()")

class CandleBuilder(Component):

  def started(self, *args):
    print("CandleBuilder started")

  def tick(self, event):
    print("Received tick")
