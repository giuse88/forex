from abc import ABCMeta, abstractmethod

from trading.emitter.component import Component, listen_on
from trading.events.event import Signal, Order, FillEvent
from trading.utils.logger import Logger

class Executor(Component, Logger):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(Executor, self).__init__()
        self.logger.info("Execution handler created")

    @listen_on('order')
    def on_order(self, order):
        self.execute_order(self, order)

    @abstractmethod
    def execute_order(self, order):
        raise NotImplementedError("Should implement execute_order()")


class DummyExecutor(Executor):

    def __init__(self):
        super(DummyExecutor, self).__init__()

    def execute_order(self, order):
        self.logger.info("Processing: " + str(order))
        self.emit()
