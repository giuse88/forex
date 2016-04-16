from datetime import datetime
from ..utils.time import stringify


class Candle:
    def __init__(self, timestamp, timeframe, sorted_values):
        self.timestamp = timestamp
        self.timeframe = timeframe
        self.open_price = sorted_values[0]
        self.close_price = sorted_values[len(sorted_values) - 1]
        self.high = max(sorted_values)
        self.low = min(sorted_values)

    def __str__(self):
        return str(datetime.fromtimestamp(self.timestamp)) \
               + " { H:" + str(self.high) + " L:" + str(self.low) + " O: " \
               + str(self.open_price) + " C: " + str(self.close_price) + " }"

    def __repr__(self):
        return self.__str__()


class Price(object):
    def __init__(self, ask=0, bid=0):
        self.ask = float(ask)
        self.bid = float(bid)

    @property
    def mid(self):
        return (self.ask + self.bid) / 2

    def __str__(self):
        return "Ask:{:.6f} Bid:{:.6f} Mid{:.6f}".format(self.ask, self.bid, self.mid)

    def __repr__(self):
        return self.__str__()


class Tick:
    def __init__(self, **args):
        self.ask = args['ask']
        self.bid = args['bid']
        self.timestamp = args['timestamp']
        self.ask_volume = args['ask_volume']
        self.bid_volume = args['bid_volume']
        self.symbol = args['symbol']

    def __str__(self):
        return "Tick({:s}): Symbol={:s}, Ask={:.6f} Bid {:.6f} Ask volume {:.6f} Bid volume {:.6f} " \
            .format(stringify(self.timestamp), self.symbol, self.ask, self.bid, self.ask_volume, self.bid_volume)
