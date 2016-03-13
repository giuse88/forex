from trading.emitter.component import Component, listen_on
from trading.events.event import Signal, Order, Trade
from trading.utils.logger import Logger
from trading.core import Price
from decimal import Decimal as D, getcontext

#BID is the sell price
#ASK is the buy price
# ASK > BID
# EURUSD --> 1.1147 1.1149 spread 2 buy 1.1149 sell 1.1147

class Portafolio(Component, Logger):

    def __init__(self, symbols, initial_capital):
        super(Portafolio, self).__init__()
        self.logger.info("Portafolio created")
        self.symbols = symbols
        self.initial_capital = initial_capital
        self.positions = []

    @listen_on('signal')
    def on_signal(self, signal):
        self.logger.info("Processing " + str(signal))
        self.emit(Order(signal.symbol, 'MKT', 1, 'BUY'))

    @listen_on('FillEvent')
    def on_fill_event(self, event):
        self.logger.info("Processing " + str(event))

class Position(object):

    def __init__(self, symbol, current_price):
        self.symbol = symbol
        self.trades = []
        self.current_price = current_price
        self._reset_fields()
        self.state = 'INIT'

    def _reset_fields(self):
        self.units_bought = 0
        self.units_sold = 0
        self.amount_bought = D(0)
        self.amount_sold = D(0)

    @property
    def units(self):
        return  self.units_bought - self.units_sold;

    @property
    def profit(self):
        return round(self.holding - self.exposure, 4)

    @property
    def exposure(self):
        return round(self.amount_bought - self.amount_sold, 4)

    @property
    def holding(self):
        if self.units > 0:
            return round(self.units * self.current_price.bid, 4)
        else:
            return round(self.units * self.current_price.ask, 4)

    @property
    def pips(self):
        if self.units is not 0:
            return int((D(self.profit) / abs(self.units) / D(0.0001)).to_integral())
        return 0

    @listen_on('tick')
    def update_holdings(self, tick):
        if tick.symbol is self.symbol:
            self.update_current_price(Price(tick.ask, tick.bid))

    def update_current_price(self, new_price):
        self.current_price = new_price
        self.recalculate_position()

    def add_trade(self, trade):
        if self.is_closed():
            raise Exception("Position closed")
        else:
            self.trades.append(trade)
            self.recalculate_position()

    def recalculate_position(self):
        self._reset_fields()

        for trade in self.trades:
            if trade.side is 'BUY':
                self.units_bought += trade.units
                self.amount_bought = self.amount_bought + trade.units * trade.fill_price
            elif trade.side is 'SELL':
                self.units_sold += trade.units
                self.amount_sold = self.amount_sold + trade.units * trade.fill_price

        if self.units == 0 :
            self.state = 'CLOSED'
        else:
            self.state = 'OPEN'

    def empty(self):
        return len(self.trades) == 0

    def is_open(self):
        return not self.is_closed()

    def is_closed(self):
        return self.state == 'CLOSED'
