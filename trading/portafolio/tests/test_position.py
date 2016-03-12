import unittest
from unittest.mock import Mock
from datetime import datetime
from decimal import Decimal as D

from ..portafolio import  Position, Trade, Price

class TestPosition(unittest.TestCase):

    def setUp(self):
        self.symbol = 'GDBUSD'
        current_price = Price(D(1.5156), D(1.5156))
        self.trade = Trade(datetime.utcnow(), self.symbol, D(1.5166), 2000, 'BUY')
        self.position = Position(self.symbol, current_price)

    def test_a_new_positioon_is_empty(self):
        self.assertTrue(self.position.empty())

    def test_a_position_has_a_symbol(self):
        self.assertEqual(self.position.symbol, self.symbol)

    def test_initialization(self):
        self.assertEqual(self.position.pips, 0)
        self.assertEqual(self.position.total_units, 0)
        self.assertEqual(self.position.holding, 0)
        self.assertEqual(self.position.profit_base, 0)
        self.assertEqual(self.position.profit_perc, 0)

    def test_open_long_position(self):
        self.position.add_trade(self.trade)
        self.assertFalse(self.position.empty())
        self.assertEquals(self.position.pips, -10)

    def test_update_position(self):
        self.position.add_trade(self.trade)
        self.position.update_current_price(Price(D(1.5151), D(1.5152)))
        self.assertEquals(self.position.pips, -15)

    def test_close_position(self):
        self.position.add_trade(Trade(datetime.utcnow(), self.symbol, D(1.5176), 2000, 'SELL'))
        self.assertEquals(self.position.pips, -20)
        self.assertTrue(self.position.is_closed())

