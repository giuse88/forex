import unittest
from unittest.mock import Mock
from datetime import datetime

from ..portafolio import  Position, Trade

class TestTrade(unittest.TestCase):

    def setUp(self):
        self.trade = Trade(datetime.utcnow(), 'GDBUSD', 34.56, 1000, 'BUY')

    def test_trade_has_timestamp(self):
        self.assertIsNotNone(self.trade.timestamp)

    def test_trade_has_fill_price(self):
        self.assertIsNotNone(self.trade.fill_price)

    def test_trade_has_symbol(self):
        self.assertIsNotNone(self.trade.symbol)

    def test_trade_has_side(self):
        self.assertIsNotNone(self.trade.side)
