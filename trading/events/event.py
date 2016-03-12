from datetime import datetime
from trading.utils.time import stringify
from trading.emitter.component import Event

class BaseEvent(Event):

    def __init__(self):
      super(BaseEvent, self).__init__()
      self.event_timestamp = datetime.utcnow()

    def __str__(self):
        return "Base Event"

class Tick(BaseEvent):

  def __init__(self, **args):
      super(BaseEvent, self).__init__()
      self.type = 'Tick'
      self.ask = args['ask']
      self.bid = args['bid']
      self.timestamp = args['timestamp']
      self.ask_volume = args['ask_volume']
      self.bid_volume = args['bid_volume']
      self.symbol = args['symbol']

  def __str__(self):
    return "Tick({:s}): Symbol={:s}, Ask={:.6f} Bid {:.6f} Ask volume {:.6f} Bid volume {:.6f} " \
            .format(stringify(self.timestamp), self.symbol, self.ask, self.bid, self.ask_volume, self.bid_volume )

class MarketEvent(BaseEvent):

    def __init__(self):
        self.type = 'MARKET'
        self.timestamp = datetime.utcnow()

    def __str__(self):
        return self.type + " generated at " + self.timestamp


class Signal(Event):
    """
    Handles the event of sending a Signal from a Strategy object.
    This is received by a Portfolio object and acted upon.
    """

    def __init__(self, symbol, signal_type, strength):
        """
        Initialises the SignalEvent.
        Parameters:
            - strategy_id : The unique identifier for the strategy that
            generated the signal.
           - symbol : The ticker symbol, e.g. ’GOOG’.
           - datetime : The timestamp at which the signal was generated.
           - signal_type : ’LONG’ or ’SHORT’.
           - strength : An adjustment factor "suggestion" used to scale
            quantity at the portfolio level. Useful for pairs strategies.
        """

        self.type = 'SIGNAL'
        self.signal_type = signal_type
        self.strength = strength
        self.symbol = symbol

    def __str__(self):
        return "Signal: Symbol={:s}, Type={:s}, Strenght={:.2f}".format(self.symbol, self.signal_type, self.strength)

class OrderEvent(Event):
    """
    Handles the event of sending an Order to an execution system.
    The order contains a symbol (e.g. GOOG), a type (market or limit),
    """

    def __init__(self, symbol, order_type, quantity, direction):
        """
        Initialises the order type, setting whether it is
        a Market order (’MKT’) or Limit order (’LMT’), has
        a quantity (integral) and its direction (’BUY’ or
        ’SELL’).
        Parameters:
            symbol - The instrument to trade.
            order_type - ’MKT’ or ’LMT’ for Market or Limit.
            quantity - Non-negative integer for quantity.
            direction - ’BUY’ or ’SELL’ for long or short.
        """
        self.type = 'ORDER'
        self.symbol = symbol
        self.order_type = order_type
        self.quantity = quantity
        self.direction = direction

    def __str__(self):
        return "Order: Symbol=%s, Type=%s, Quantity=%s, Direction=%s" % (self.symbol, self.order_type, self.quantity, self.direction)

class FillEvent(Event):
    """
    Encapsulates the notion of a Filled Order, as returned
    from a brokerage. Stores the quantity of an instrument
    actually filled and at what price. In addition, stores
    the commission of the trade from the brokerage.
    """

    def __init__(self, symbol, exchange, quantity, direction, fill_cost, commission=None):
        """
        Initialises the FillEvent object. Sets the symbol, exchange, quantity, direction, cost of fill and an optional commission.
        If commission is not provided, the Fill object will
        calculate it based on the trade size and Interactive
        Brokers fees.
        Parameters:
            timeindex - The bar-resolution when the order was filled.
            symbol - The instrument which was filled.
            exchange - The exchange where the order was filled.
            quantity - The filled quantity.
            direction - The direction of fill (’BUY’ or ’SELL’)
            fill_cost - The holdings value in dollars.
            commission - An optional commission
        """
        self.type = 'FILL'
        self.symbol = symbol
        self.exchange = exchange
        self.quantity = quantity
        self.direction = direction
        self.fill_cost = fill_cost
        self.commission = commission

    def __str__(self):
        return "Signal: Symbol={:s}, Exchange={:s}, Quantity={:d}, Direction={:s}, Fill cost={:.2f} " \
            .format(self.symbol, self.exchange, self.quantity, self.direction, self.fill_cost)


if __name__ == "__main__":
    event = BaseEvent();
    print(str(event))
    print(str(tick(ask=1.11767, bid=1.11763, ask_volume=2.3200, bid_volume=1.0000, timestamp=54353, symbol='USDEUR')))
#    print("Signal event:" + str(SignalEvent('EURUSD', 'LONG', 5.5)))
#    print("Order event:" + str(OrderEvent('EURUSD', 'MKT', 1, 'BUY')))
#    print("Fill event:" + str(FillEvent('EURUSD', 'SWISS', 1, 'BUY', 2.5)))

