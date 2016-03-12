import unittest
from unittest.mock import Mock

from ..component import Component, Event, listen_on

class Test(Event):
    """ Test Event """

    def __init__(self):
        self.field = 'this is a test field'

    def __str__(self):
        return str(self.field)

class Test_1(Test):
    """ test 1 """

class Listener(Component):

    @listen_on('test')
    @listen_on('test_1')
    def on_test(self, event):
      pass

    @listen_on('test_1')
    def second_event(self, event):
      pass

class TestComponent(unittest.TestCase):

  def setUp(self):
    self.component_under_test = Listener()
    self.on_test_mock = Mock(return_value=None)
    self.on_second_event_mock = Mock(return_value=None)
    Component._emitter._events['test'] = [self.on_test_mock]
    Component._emitter._events['test_1'] = [self.on_test_mock, self.on_second_event_mock]

  def tearDown(self):
    self.on_test_mock.reset_mock()
    self.on_second_event_mock.reset_mock()

  def test_on_test_is_called(self):
    self.component_under_test.emit(Test())
    self.on_test_mock.assert_called_once()

  def test_with_multiple_decorators(self):
    self.component_under_test.emit(Test_1())
    self.component_under_test.emit(Test())
    self.assertEqual(self.on_test_mock.call_count, 2)

  def test_with_multiple_methods(self):
    self.component_under_test.emit(Test_1())
    self.assertEqual(self.on_test_mock.call_count, 1)
    self.assertEqual(self.on_second_event_mock.call_count, 1)

  def test_case_insentive_event(self):
    class test_1(Event):
      pass
    self.component_under_test.emit(test_1())
    self.assertEqual(self.on_second_event_mock.call_count, 1)
