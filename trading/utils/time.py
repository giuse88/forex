import time
from datetime import  datetime
from trading.settings import DATETIME_FORMAT

def toUTCTimestamp(timeStr):
 return time.mktime(datetime.strptime(timeStr, DATETIME_FORMAT).timetuple())

def stringify(timestamp):
  return str(datetime.fromtimestamp(timestamp))
