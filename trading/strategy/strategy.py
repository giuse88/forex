from abc import ABCMeta, abstractmethod

from trading.emitter.component import Component, listen_on
from trading.events.event import Signal

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
        print("Processing " + str(event))
        if event.symbol is self.symbol:
            self.tick_counter = ( self.tick_counter + 1 ) % self.ticks
            self.calculate_signals()

    def calculate_signals(self):
        if self.tick_counter is 0 :
            signal = Signal(self.symbol, 'LONG', 0.5)
            self.emit(signal)

class Portafolio(Component):

    def __init__(self, symbol):
        super(Portafolio, self).__init__()

    @listen_on('signal')
    def on_signal(self, signal):
        print("Processing " + str(signal))
