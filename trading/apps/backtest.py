#!/usr/bin/env python3

from circuits import Debugger

from trading.DataSource.CSVTickDataSource import CSVTickDataSource
from trading.strategy.strategy import CandleBuilder


def main():
  print("Backtest trading system v 0.1")
  source = CSVTickDataSource('../data/', 'EURUSD', '*.small.csv', 1)
  candleBuilder = CandleBuilder()
  (source + candleBuilder).run()

if __name__ == '__main__':
  main()
