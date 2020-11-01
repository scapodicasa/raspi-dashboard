from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger

import logging
logger = logging.getLogger(__name__)


class ClockService:

    _scheduler = None
    _func = None
    _running = None

    def __init__(self, func):
        self._scheduler = AsyncIOScheduler()
        self._func = func
        self._running = False

    def start(self):
        logger.info("Starting Clock")

        if not self._scheduler.running:
            logger.debug("Starting clock scheduler")
            self._scheduler.start()

        self._running = True
        self._do()

    def is_running(self):
        return self._running

    def stop(self):
        logger.info("Stopping Clock")
        self._running = False

    def _do(self):
        if self._running:
            logger.info("Executing payload.")

            self._func()

            if len(self._scheduler.get_jobs()) == 0:
                logger.debug("Scheduling next clock iteration")

                now = datetime.now()
                now = now + timedelta(minutes=1)
                self._scheduler.add_job(self._do, DateTrigger(datetime(
                    now.year, now.month, now.day, now.hour, now.minute)), misfire_grace_time=604800)
            else:
                logger.debug(
                    "Next iteration not scheduled because of some jobs are already scheduled")
        else:
            logger.debug("Payload not executed because Clock is not running.")
