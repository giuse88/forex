from abc import ABCMeta, abstractmethod

from trading.emitter.component import Component, listen_on
from trading.events.event import SignalEvent

class Strategy(Component):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Strategy, self).__init__()

    @abstractmethod
    def calculate_signals(self):
        raise NotImplementedError("Should implement calculate_signals()")

class BuyEveryNTicks(Component):

    def __init__(self, symbol, ticks):
        super(BuyEveryNTicks, self).__init__()
        self.symbol = symbol
        self.tick_counter = 0
        self.ticks = ticks;

    @listen_on('tick')
    def on_tick(self, event):
        if event.symbol is self.symbol:
            self.tick_counter = ( self.tick_counter + 1 ) % self.ticks
            self.calculate_signals()

    def calculate_signals(self):
        if self.tick_counter is 0 :
            signal = SignalEvent(self.symbol, 'LONG', 0.5)
            print("Emiting : " + str(signal))
            self.emit(signal)
