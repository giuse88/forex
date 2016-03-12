#!/usr/bin/env python3

from trading.strategy.strategy import BuyEveryNTicks, Portafolio, Executor
from trading.DataSource.CSVTickDataSource import CSVTickDataSource

class BackTest(object):

  def __init__(self):
      symbol = 'EURUSD'
      self.source = CSVTickDataSource('../data/', symbol, '*.small.csv')
      self.strategy = BuyEveryNTicks(symbol, 3)
      self.portafolio = Portafolio(symbol)
      self.executor = Executor()

  def start(self):
      self.source.read_data()

def main():
    print("Backtest trading system v 0.1")
    BackTest().start()

if __name__ == '__main__':
  main()
