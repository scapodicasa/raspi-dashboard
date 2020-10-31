import time

import logging
logger = logging.getLogger(__name__)


def print():
    logger.info(time.strftime("%H:%M"))
