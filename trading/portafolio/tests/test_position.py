import unittest
from unittest.mock import Mock
from datetime import datetime

from decimal import Decimal as D, getcontext

#getcontext().prec = 4

from ..portafolio import  Position, Trade, Price

class TestPosition(unittest.TestCase):

    def setUp(self):
        self.symbol = 'GDBUSD'
        current_price = Price(D(1.1583), D(1.1581))

        self.long_trade = Trade(
                timestamp=datetime.utcnow(),
                symbol=self.symbol,
                fill_price=D(1.1583),
                units=10000,
                side='BUY',
                commission=0,
                exchange='FX')

        self.short_trade = Trade(
                timestamp=datetime.utcnow(),
                symbol=self.symbol,
                fill_price=D(1.1581),
                units=10000,
                side='SELL',
                commission=0,
                exchange='FX')

        self.position = Position(self.symbol, current_price)

    def test_a_new_positioon_is_empty(self):
        self.assertTrue(self.position.empty())

    def test_a_position_has_a_symbol(self):
        self.assertEqual(self.position.symbol, self.symbol)

    def test_initialization(self):
        self.assertEqual(self.position.pips, 0)
        self.assertEqual(self.position.units, 0)

    def test_open_long_position(self):
        self.position.add_trade(self.long_trade)
        self.assertTrue(self.position.is_open())
        self.assertEqual(self.position.units, 10000)
        self.assertEqual(self.position.holding, round(D(11581.00), 4))
        self.assertEqual(self.position.exposure, round(D(11583.00), 4))
        self.assertEqual(self.position.profit, round(D(-2), 4))
        self.assertEquals(self.position.pips, -2)

    def test_open_short_positon(self):
        self.position.add_trade(self.short_trade)
        self.assertTrue(self.position.is_open())
        self.assertEqual(self.position.units, -10000)
        self.assertEqual(self.position.holding, round(D(-11583.00), 4))
        self.assertEqual(self.position.exposure, round(D(-11581.00), 4))
        self.assertEqual(self.position.profit, round(D(-2), 4))
        self.assertEquals(self.position.pips, -2)

    def test_update_position(self):
        self.position.add_trade(self.long_trade)
        self.position.update_current_price(Price(D(1.1586), D(1.1585)))
        self.assertEqual(self.position.units, 10000)
        self.assertEqual(self.position.holding, round(D(11585.00), 4))
        self.assertEqual(self.position.exposure, round(D(11583.00), 4))
        self.assertEqual(self.position.profit, round(D(2), 4))
        self.assertEquals(self.position.pips, 2)

    def test_close_position(self):
        self.position.add_trade(self.long_trade)
        self.position.add_trade(self.short_trade)
        self.assertFalse(self.position.is_open())
        self.assertTrue(self.position.is_closed())
        self.assertEqual(self.position.units, 0)
        self.assertEqual(self.position.holding, round(D(0), 4))
        self.assertEqual(self.position.exposure, round(D(2), 4))
        self.assertEqual(self.position.profit, round(D(-2), 4))

