from datetime import datetime

import time
from trading.settings import DATETIME_FORMAT


def to_utc_timestamp(timeStr):
    return time.mktime(from_time_string(timeStr).timetuple())


def from_time_string(time_str):
    if '.' not in time_str:
        time_str += '.0'
    return datetime.strptime(time_str, DATETIME_FORMAT)


def stringify(timestamp):
    return str(datetime.fromtimestamp(timestamp))
