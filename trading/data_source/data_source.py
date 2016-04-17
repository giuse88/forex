import csv
import os
from datetime import date, timedelta

from trading.core import Candle, Tick, Price
from trading.settings import TEMPLATE_FILE_NAME
from trading.utils.time_util import to_utc_timestamp

SATURDAY = 5


class CSVFormatter(object):
    COLUMN_TIME = 0
    COLUMN_ASK = 1
    COLUMN_BID = 2
    COLUMN_ASK_VOLUME = 3
    COLUMN_BID_VOLUME = 4


class TimeFrame(object):
    TICK = 0
    S_30 = 30
    M1 = 60
    M2 = 120
    M5 = 300
    M10 = 600
    M15 = 900
    M30 = 1800
    H1 = 3600
    H4 = 14400
    D1 = 86400


class PriceAggregator(object):
    ASK = 'ask'
    BID = 'bid'
    MID = 'mid'


def days(start, end):
    if start > end:
        return
    end = end + timedelta(days=1)
    today = date.today()
    while start != end:
        if start.weekday() != SATURDAY and start != today:
            yield start
        start = start + timedelta(days=1)


def data_source(**kwargs):
    symbol = kwargs.get("symbol") or "EURUSD"
    start = kwargs["start"]
    end = kwargs["end"]

    if kwargs.get("timeframe") is None:
        timeframe = TimeFrame.M10
    else:
        timeframe = kwargs.get('timeframe')

    data_folder = kwargs.get("folder") or "./data"
    price_aggregator = kwargs.get("price_aggregator") or PriceAggregator.BID

    def price(p):
        return getattr(p, price_aggregator)

    def csv_path(day):
        file_name = TEMPLATE_FILE_NAME.format(symbol, day.year, day.month, day.day)
        return os.path.join(data_folder, symbol, file_name)

    def forge_tick(row):
        tick = dict()
        tick['ask'] = float(row[CSVFormatter.COLUMN_ASK])
        tick['bid'] = float(row[CSVFormatter.COLUMN_BID])
        tick['ask_volume'] = int(row[CSVFormatter.COLUMN_ASK_VOLUME])
        tick['bid_volume'] = int(row[CSVFormatter.COLUMN_BID_VOLUME])
        tick['symbol'] = symbol
        tick['timestamp'] = to_utc_timestamp(row[CSVFormatter.COLUMN_TIME])
        return Tick(**tick)

    previous_key = None
    ticks = []

    for day in days(start, end):
        with open(csv_path(day), 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=',')
            for row in reader:
                if isinstance(row[CSVFormatter.COLUMN_ASK], str) and \
                                row[CSVFormatter.COLUMN_ASK].lower() == 'ask':
                    continue
                if timeframe == TimeFrame.TICK:
                    yield forge_tick(row)
                else:
                    ts = to_utc_timestamp(row[CSVFormatter.COLUMN_TIME])
                    key = int(ts - (ts % timeframe))
                    if previous_key != key and previous_key is not None:
                        yield Candle(symbol, previous_key, timeframe, ticks)
                        ticks = []
                    ticks.append(price(Price(row[CSVFormatter.COLUMN_ASK], row[CSVFormatter.COLUMN_BID])))
                    previous_key = key

            if timeframe != TimeFrame.TICK:
                yield Candle(symbol, previous_key, timeframe, ticks)


def main():
    for d in data_source(
            folder='../data',
            symbol='EURUSD',
            timeframe=TimeFrame.M1,
            start=date(2015, 1, 1),
            price_aggregator=PriceAggregator.MID,
            end=date(2015, 1, 10)):
        print(d)


if __name__ == "__main__":
    main()
