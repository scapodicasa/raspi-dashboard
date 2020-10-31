import logging
logger = logging.getLogger(__name__)


def print(result, without_display=False):
    logger.info(result)

    if without_display:
        return
