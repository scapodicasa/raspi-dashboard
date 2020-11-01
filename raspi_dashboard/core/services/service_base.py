from datetime import datetime, timedelta
from enum import Enum

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

from ..publisher import Publisher

import logging
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
        logger.info("Starting")

        if not self._scheduler.running:
            logger.debug("Starting scheduler")
            self._scheduler.start()

        self._running = True
        self._do()

    def is_running(self):
        return self._running

    def stop(self):
        logger.info("Stopping")
        self._running = False

    def get_next_trigger(self):
        raise Exception('get_next_trigger() not implemented')

    def _do(self):
        if self._running:
            logger.info("Executing payload.")

            self.dispatch(ServiceBase.Events.ON_TRIGGER)

            if len(self._scheduler.get_jobs()) == 0:
                logger.debug("Scheduling next iteration")

                self._scheduler.add_job(
                    self._do, self.get_next_trigger(), misfire_grace_time=604800)
            else:
                logger.debug(
                    "Next iteration not scheduled because of some jobs are already scheduled")
        else:
            logger.debug(
                "Payload not executed because service is not running.")
