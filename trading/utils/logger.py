import logging
import sys

class Logger(object):
    TEMPLATE = '%(asctime)s - %(levelname)s - %(name)s -  %(message)s'

    def __init__(self):
        super(Logger, self).__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
        out_hdlr = logging.StreamHandler(sys.stdout)
        out_hdlr.setFormatter(logging.Formatter(Logger.TEMPLATE))
        out_hdlr.setLevel(logging.INFO)
        self.logger.addHandler(out_hdlr)
        self.logger.setLevel(logging.INFO)
