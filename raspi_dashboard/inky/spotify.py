from . import Printer

import logging
logger = logging.getLogger(__name__)


class SpotifyPrinter(Printer):
    _result = None

    def __init__(self, display_mode, result):
        Printer.__init__(self, display_mode)
        self._result = result

    def print_console(self):
        logger.info(self._result)

    def print_display(self, inky_display):
        logger.warning("Printing on display for Spotify not yet implemented.")
