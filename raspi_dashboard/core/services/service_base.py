from datetime import datetime, timedelta
from enum import Enum

import apscheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from ..publisher import Publisher

import logging
logging.getLogger(apscheduler.__name__).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class ServiceBase(Publisher):

    _scheduler = None
    _running = None

    class Events(Enum):
        ON_TRIGGER = 'on_trigger'

    def __init__(self):
        Publisher.__init__(self, events=[mode for mode in self.Events])
        self._internal_init()

    def _internal_init(self):
        self._scheduler = AsyncIOScheduler()
        self._running = False

    def start(self):
        logger.info(f"Starting {self.__class__.__name__}")

        if not self._scheduler.running:
            logger.debug(f"Starting {self.__class__.__name__} scheduler")
            self._scheduler.start()

        self._running = True
        self._do()

    def is_running(self):
        return self._running

    def stop(self):
        logger.info(f"Stopping {self.__class__.__name__}")
        self._running = False

    def get_next_trigger(self):
        raise Exception('get_next_trigger() not implemented')

    def _do(self):
        if self._running:
            logger.info(f"Executing {self.__class__.__name__} payload.")

            self.dispatch(ServiceBase.Events.ON_TRIGGER)

            if len(self._scheduler.get_jobs()) == 0:
                logger.debug(
                    f"Scheduling {self.__class__.__name__} next iteration")

                self._scheduler.add_job(
                    self._do, self.get_next_trigger(), misfire_grace_time=604800)
            else:
                logger.debug(
                    f"Next iteration not scheduled by {self.__class__.__name__} because of some jobs are already scheduled")
        else:
            logger.debug(
                f"Payload not executed by {self.__class__.__name__} because service is not running.")
