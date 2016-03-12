#!/usr/bin/env python3

from trading.DataSource.CSVTickDataSource import CSVTickDataSource
from trading.strategy.strategy import CandleBuilder

class BackTest(object):

  def __init__(self):
    self.source = CSVTickDataSource('../data/', 'EURUSD', '*.small.csv', 1)
    self.candleBuilder = CandleBuilder()

  def start(self):
    self.source.read_data()

def main():
  print("Backtest trading system v 0.1")
  BackTest().start()


if __name__ == '__main__':
  main()
