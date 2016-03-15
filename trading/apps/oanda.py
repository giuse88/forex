#!/usr/bin/env python3

from trading.DataSource.OANDATicker import OANDATicker
from trading.portafolio.portafolio import Portafolio
from trading.strategy.strategy import BuyEveryNTicks
from trading.executor.executor import Executor, DummyExecutor

class OANDA(object):

  def __init__(self):
      symbol = 'EUR_USD'
      self.source = OANDATicker([symbol])
      self.strategy = BuyEveryNTicks(symbol, 3)
      self.portafolio = Portafolio([symbol], 100000)
      self.executor = DummyExecutor()

  def start(self):
      self.source.connect()

def main():
    print("Backtest trading system v 0.1")
    OANDA().start()

if __name__ == '__main__':
  main()
