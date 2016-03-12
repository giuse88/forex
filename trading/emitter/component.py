from pyee import EventEmitter

EVENT_LIST_IDENTIFIER = "_component_emitter_on"

class Event(object):
    pass

class Component(object):
    _emitter = EventEmitter()
    def __init__(self):
        for attr_name in dir(self):
            method = getattr(self, attr_name)
            if hasattr(method, EVENT_LIST_IDENTIFIER):
                for event in method._component_emitter_on:
                    self._emitter.on(event.lower(), method)
            self.attr_name = method

    def emit(self, event):
        event_type = event.__class__.__name__.lower()
        Component._emitter.emit(event_type, event)

def listen_on(event):
    def listen_on_decorator(func):
        func._component_emitter_on = getattr(func, EVENT_LIST_IDENTIFIER, []) + [event]
        return func
    return listen_on_decorator

