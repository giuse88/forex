from abc import ABCMeta, abstractmethod
from decimal import Decimal as D
import time

from trading.emitter.component import Component, listen_on
from trading.events.event import Signal, Order, Trade
from trading.utils.logger import Logger
from trading.core import Price

class Executor(Component, Logger):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Executor, self).__init__()
        self.current_prices = {}
        self.logger.info("Execution handler created")

    @listen_on('tick')
    def update_current_price(self, tick):
        price = Price(tick.ask, tick.bid)
        self.logger.info("Updating price for {:s} {:s}".format(tick.symbol, str(price)))
        self.current_prices[tick.symbol] = price

    @listen_on('order')
    def on_order(self, order):
        self.execute_order(order)

    @abstractmethod
    def execute_order(self, order):
        raise NotImplementedError("Should implement execute_order()")

class DummyExecutor(Executor):

    def execute_order(self, order):
        self.logger.info("Processing: " + str(order))
        if len(self.current_prices) is 0:
            self.logger.warn("Missing current price. Cannot execute trade")
            return

        if order.side == 'BUY':
            price = self.current_prices[order.symbol].ask
        else:
            price = self.current_prices[order.symbol].bid

        self.emit(
            Trade(
                timestamp=time.time(),
                symbol=order.symbol,
                fill_price=round(D(price), 6),
                units=order.quantity,
                side=order.side,
                commission=0,
                exchange='FX'
            )
        )
