from abc import ABCMeta, abstractmethod

from trading.emitter.component import Component, listen_on
from trading.events.event import Signal, Order
from trading.utils.logger import Logger

class Strategy(Component, Logger):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Strategy, self).__init__()
        self.logger.info("Strategy object created")

    @abstractmethod
    def calculate_signals(self):
        raise NotImplementedError("Should implement calculate_signals()")

class BuyEveryNTicks(Strategy):

    def __init__(self, symbol, ticks):
        super(BuyEveryNTicks, self).__init__()
        self.symbol = symbol
        self.tick_counter = 0
        self.ticks = ticks;

    @listen_on('tick')
    def on_tick(self, event):
        self.logger.info("Processing " + str(event))
        if event.symbol is self.symbol:
            self.tick_counter = ( self.tick_counter + 1 ) % self.ticks
            self.calculate_signals()

    def calculate_signals(self):
        if self.tick_counter is 0 :
            signal = Signal(self.symbol, 'LONG', 0.5)
            self.emit(signal)

class Portafolio(Component, Logger):

    def __init__(self, symbol):
        super(Portafolio, self).__init__()
        self.logger.info("Portafolio created")
        self.symbol = symbol

    @listen_on('signal')
    def on_signal(self, signal):
        self.logger.info("Processing " + str(signal))
        self.emit(Order(self.symbol, 'MKT', 1, 'BUY'))

class Executor(Component, Logger):

    def __init__(self):
        super(Executor, self).__init__()
        self.logger.info("Execution handler created")

    @listen_on('order')
    def on_order(self, order):
        self.logger.info("Processing: " + str(order))
