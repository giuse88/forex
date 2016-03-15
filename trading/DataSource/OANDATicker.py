import requests
import time
from datetime import datetime
import json
from trading.utils.validation import isFloat, isValidDate
from trading.events.event import Tick
from trading.utils.time import toUTCTimestamp
from trading.DataSource.DataSource import DataSource
from trading.utils.logger import Logger

class OANDATicker(DataSource, Logger):
    def __init__(self, instruments):
        super(OANDATicker, self).__init__()
        self.domain = 'api-fxpractice.oanda.com'
        self.access_token = '4e8c5da75cbc23c5499ed9911f713699-78a54194e5457e0a3f7b05e0d10e06d0'
        self.instruments = instruments
        self.last_tick = None

    def connect(self):
        while True:
            try:
                url = "https://" + self.domain + "/v1/prices"
                headers = {'Authorization' : 'Bearer ' + self.access_token}
                params = {'instruments' : self.instruments}
                r = requests.get(url, headers=headers, params=params).json()
                tick = self.forge_tick(r)
                if tick != self.last_tick:
                    self.emit(Tick(**tick))
                    self.last_tick = tick
                time.sleep(1)
            except Exception as e:
                print("Caught exception when connecting to stream\n" + str(e))

    def forge_tick(self, response):
        price = response['prices'][0]
        tick = {}
        tick['ask'] = price['ask']
        tick['bid'] = price['bid']
        tick['ask_volume'] = -1
        tick['bid_volume'] = -1
        tick['symbol'] = price['instrument']
        t = time.mktime(datetime.strptime(price['time'], '%Y-%m-%dT%H:%M:%S.%fZ' ).timetuple())
        tick['timestamp'] = int(t)
        return tick


if __name__ == "__main__":
    instruments = ['EUR_USD']
    s = StreamingForexPrices(instruments)
    s.connect_to_stream()
