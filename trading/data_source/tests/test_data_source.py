import unittest
from datetime import date, datetime, timedelta

from trading.core import Candle
from trading.data_source import data_source, PriceAggregator, TimeFrame
from trading.utils.time_util import to_utc_timestamp

candle_0 = Candle('EURUSD', to_utc_timestamp("2015-01-01 00:00:00.0"), TimeFrame.M1,
                  [1.21066, 1.21067, 1.21060, 1.21059, 1.21059])
candle_1 = Candle('EURUSD', to_utc_timestamp("2015-01-01 00:01:00.0"), TimeFrame.M1,
                  [1.2106, 1.21067, 1.21066, 1.21065, 1.21062, 1.21058, 1.21058,
                   1.21058, 1.21062, 1.21062, 1.21064, 1.21064, 1.21063, 1.21066])
candle_2 = Candle('EURUSD', to_utc_timestamp("2015-01-01 00:02:00.0"), TimeFrame.M1,
                  [1.21061, 1.2106, 1.2106, 1.2106, 1.2106, 1.21061, 1.21058, 1.21058])

last_candle = Candle('EURUSD', to_utc_timestamp("2015-01-01 01:59:00.0"), TimeFrame.M1, [
    1.2091, 1.2091, 1.2091, 1.2091, 1.20912, 1.20912, 1.20912, 1.20912, 1.20905, 1.20904, 1.20904,
    1.20907, 1.2091, 1.20907, 1.20907, 1.20911, 1.20905, 1.20898, 1.20898, 1.20898, 1.20895, 1.20895,
    1.20894, 1.20894, 1.20894, 1.20894, 1.20894, 1.20892, 1.20892, 1.20894, 1.20894, 1.20894, 1.20894,
    1.20894, 1.20894, 1.20894, 1.20894, 1.20894, 1.20894, 1.20894, 1.20894, 1.20893, 1.20892, 1.20892,
    1.20893, 1.20893, 1.20893, 1.20885, 1.20881, 1.20881, 1.20879, 1.2088, 1.20879, 1.20879, 1.2088,
    1.20882, 1.20883, 1.20881, 1.20879, 1.20876, 1.20878, 1.20878, 1.20879, 1.20879, 1.20879, 1.2088,
    1.2088, 1.2088, 1.2088, 1.2088, 1.20879])


class Test1MCandle(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime(2015, 1, 1, 0, 0, 0, 0)
        self.candles_1M = [x for x in data_source(
            folder='fixtures',
            symbol='EURUSD',
            timeframe=TimeFrame.M1,
            start=date(2015, 1, 1),
            price_aggregator=PriceAggregator.ASK,
            end=date(2015, 1, 1))]

    def tearDown(self):
        pass

    def test_first_3_candles(self):
        self.assertEqual(candle_0, self.candles_1M[0])
        self.assertEqual(candle_1, self.candles_1M[1])
        self.assertEqual(candle_2, self.candles_1M[2])

    def test_all_candles_have_the_correct_timestamp(self):
        for i, c in enumerate(self.candles_1M):
            self.assertEqual(datetime.fromtimestamp(c.timestamp), self.start_time + timedelta(minutes=i))

    def test_last_candle(self):
        self.assertEqual(last_candle, self.candles_1M[len(self.candles_1M) - 1])

    def test_1M_candle(self):
        self.assertEqual(len(self.candles_1M), 120)


class TestTickGenerator(unittest.TestCase):
    def setUp(self):
        self.start_time = datetime(2015, 1, 1, 0, 0, 0, 0)
        self.ticks = [x for x in data_source(
            folder='fixtures',
            symbol='EURUSD',
            timeframe=TimeFrame.TICK,
            start=date(2015, 1, 1),
            end=date(2015, 1, 1))]

    def test_first_tick(self):
        self.assertEqual(self.ticks[0].ask, 1.21066)
        self.assertEqual(self.ticks[0].bid, 1.21038)

    def test_last_tick(self):
        self.assertEqual(self.ticks[len(self.ticks) - 1].ask, 1.20879)
        self.assertEqual(self.ticks[len(self.ticks) - 1].bid, 1.20869)

    def test_ticks_candle(self):
        self.assertEqual(len(self.ticks), 3711)


class Test30MCandle(unittest.TestCase):

    def setUp(self):
        self.start_time = datetime(2015, 1, 1, 0, 0, 0, 0)
        self.candles_30M = [x for x in data_source(
            folder='fixtures',
            symbol='EURUSD',
            timeframe=TimeFrame.M30,
            start=date(2015, 1, 1),
            price_aggregator=PriceAggregator.ASK,
            end=date(2015, 1, 1))]

    def test_all_candles_have_the_correct_timestamp(self):
        for i, c in enumerate(self.candles_30M):
            print(c)
            self.assertEqual(datetime.fromtimestamp(c.timestamp), self.start_time + timedelta(minutes=i*30))

    def test_1M_candle(self):
        self.assertEqual(len(self.candles_30M), 4)


class Test1HCandle(unittest.TestCase):

    def setUp(self):
        self.start_time = datetime(2015, 1, 1, 0, 0, 0, 0)
        self.candles_1H = [x for x in data_source(
            folder='fixtures',
            symbol='EURUSD',
            timeframe=TimeFrame.H1,
            start=date(2015, 1, 1),
            price_aggregator=PriceAggregator.ASK,
            end=date(2015, 1, 1))]

    def test_all_candles_have_the_correct_timestamp(self):
        for i, c in enumerate(self.candles_1H):
            self.assertEqual(datetime.fromtimestamp(c.timestamp), self.start_time + timedelta(minutes=i*60))

    def test_1H_candle(self):
        self.assertEqual(len(self.candles_1H), 2)
