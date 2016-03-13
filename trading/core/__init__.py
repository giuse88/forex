from trading.utils.time import stringify

class Candle:

    def __init__(self, timestamp, timeframe, sortedValues):
        self.timestamp = timestamp
        self.timeframe = timeframe
        self.open_price = sortedValues[0]
        self.close_price = sortedValues[len(sortedValues) - 1]
        self.high  = max(sortedValues)
        self.low = min(sortedValues)

    def __str__(self):
        return str(datetime.fromtimestamp(self.timestamp)) \
         + " { H:" + str(self.high) + " L:" + str(self.low) + " O: " \
         + str(self.open_price) + " C: " + str(self.close_price)+ " }"

    def __repr__(self):
        return self.__str__()

class Price(object):
    def __init__(self, ask, bid):
        self.ask = ask
        self.bid = bid
