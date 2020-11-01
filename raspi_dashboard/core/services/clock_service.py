from datetime import datetime, timedelta
from enum import Enum

from apscheduler.triggers.date import DateTrigger

from . import ServiceBase

import logging
logger = logging.getLogger(__name__)


class ClockService(ServiceBase):

    def get_next_trigger(self):
        now = datetime.now()
        now = now + timedelta(minutes=1)
        return DateTrigger(datetime(now.year, now.month, now.day, now.hour, now.minute))
