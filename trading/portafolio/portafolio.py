from trading.emitter.component import Component, listen_on
from trading.events.event import Signal, Order
from trading.utils.logger import Logger
from trading.utils.time import stringify
from decimal import Decimal as D

class Portafolio(Component, Logger):

    def __init__(self, symbols, initial_capital):
        super(Portafolio, self).__init__()
        self.logger.info("Portafolio created")
        self.symbols = symbols
        self.initial_capital = initial_capital

        #self.all_positions = self.construct_all_positions()
        #self.current_positions = dict( (k,v) for k, v in \ [(s, 0) for s in self.symbol_list] )
        #self.all_holdings = self.construct_all_holdings()
        #self.current_holdings = self.construct_current_holdings()

    @listen_on('signal')
    def on_signal(self, signal):
        self.logger.info("Processing " + str(signal))
        self.emit(Order(self.symbol, 'MKT', 1, 'BUY'))

    @listen_on('tick')
    def update_holdings(self, tick):
        self.logger.info('Updating holding..')


class Trade(object):

    def __init__(self, timestamp, symbol, fill_price, units, side):
        self.timestamp = timestamp
        self.symbol = symbol
        self.fill_price = fill_price
        self.side = side
        self.units = units

    def __str__(self):
        return "Trade ({:s}) Symbol:{:s} Units:{:d} Fill Price:{:f} Side:{:s} "\
                .format(stringify(self.timestamp), self.symbol, self.units, self.fill_price, self.side)

class Price(object):
    def __init__(self, ask, bid):
        self.ask = ask
        self.bid = bid

class Position(object):

    def __init__(self, symbol, current_price):
        self.symbol = symbol
        self.trades = []
        self.current_price = current_price
        self.holding = 0
        self.exposure = 0
        self.pips = 0
        self.total_units = 0
        self.profit_base = 0
        self.profit_perc = 0

    def update_current_price(self, new_price):
        self.current_price = new_price
        self.recalculate_position()

    def add_trade(self, trade):
        self.trades.append(trade)
        self.recalculate_position()

    def recalculate_position(self):
        self.pips = 0
        self.units = 0
        for trade in self.trades:
            if trade.side is 'BUY':
                self.total_units += trade.units
                self.exposure = self.exposure + trade.units * trade.fill_price
            elif trade.side is 'SELL':
                self.total_units -= trade.units
                self.exposure = self.exposure - trade.units * trade.fill_price

        price = 0
        if self.total_units > 0:
            price = self.current_price.ask
        else:
            price = self.current_price.bid

        self.pips = self.toPip((price * self.total_units) - self.exposure )

    def exposure(self):
        return self.pips * D(0.0001) * self.units

    def holding(self):
        if self.units > 0:
            return self.units * self.current_price.ask
        else:
            return self.units * self.current_price.bid

    def empty(self):
        return len(self.trades) == 0

    def is_open(self):
        return self.units != 0

    def is_closed(self):
        return not self.is_open()

    def toPip(self, value):
        return int((D(value) / D(self.total_units) / D(0.0001)).to_integral())
