from circuits import Debugger
from datetime import timedelta, datetime
import glob, csv, os, time

from DataSource import *
from trading.utils.validation import isFloat, isValidDate
from trading.events.event import MarketEvent

class CVSTickDataSource(DataSource):
  COLUMN_TIME = 0
  COLUMN_ASK= 1
  COLUMN_BID= 2
  COLUMN_ASK_VOLUME = 3
  COLUMN_BID_VOLUME = 4

  def __init__(self, folder, file_extension='*.csv', frequency=None):
    super(CVSTickDataSource, self).__init__()
    self.folder = folder
    self.full_path = os.path.join(os.getcwd(), self.folder)
    self.frequency = frequency
    self.file_extension = file_extension

  def started(self, *args):
    print("CSVTick  data source")

    for csv_path in self._find_csv_files_within_folder():
      with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            self._process_row(row)
            if self.frequency:
              time.sleep(self.frequency)

  def _find_csv_files_within_folder(self):
    return sorted(glob.glob(os.path.join(self.full_path, self.file_extension)))

  def _validate_row(self, row):
    if len(row) != 5:
      return False

    if not isValidDate(row[CVSTickDataSource.COLUMN_TIME]):
      return False

    for x in row[1:]:
      if not isFloat(x):
        return False

    return True

  def _process_row(self, row):
    if(self._validate_row(row)):
      print(row)

if __name__ == '__main__':
    """ Test csv tick data source with mock data"""

    source = CVSTickDataSource('../data/', '*.small.csv', 0.25)
    (Debugger() + source).run()
