from datetime import datetime
from trading.settings import DATETIME_FORMAT

def isFloat(string):
  try:
    float(string)
    return True
  except ValueError:
    return False

def isValidDate(string):
  try:
    datetime.strptime(string, DATETIME_FORMAT)
    return True
  except ValueError:
    return False
