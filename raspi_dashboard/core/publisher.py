import logging
logger = logging.getLogger(__name__)


class Publisher:
    def __init__(self, events):
        self.events = {event: [] for event in events}

    def register(self, event, callback):
        self.events[event].append(callback)

    def unregister(self, event, callback):
        callbacks = self.get_callbacks(event)
        if callback in callbacks:
            callbacks.remove(callback)

    def dispatch(self, event, *args):
        for callback in self.get_callbacks(event):
            logger.debug(f"Calling callback: {callback}")
            callback(*args)

    def get_callbacks(self, event):
        res = self.events.get(event, None)
        return res if res is not None else []
