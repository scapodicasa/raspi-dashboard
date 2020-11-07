from inky import InkyPHAT, InkyMockPHAT

from .. import DisplayMode
from ...core.config import CONFIG

import logging
logger = logging.getLogger(__name__)


class PrinterBase:
    _display_mode = None
    _colour = None

    def __init__(self, display_mode):
        self._display_mode = DisplayMode(
            display_mode) if display_mode is not None else None
        self._colour = CONFIG['INKY']['colour']

    def print(self):
        self.print_console()

        if self._display_mode == DisplayMode.NO:
            return

        inky_display = self._get_inky()

        if self._display_mode == DisplayMode.MOCK:
            self.print_display(inky_display)

            logger.info("Press Ctrl+C or close window to exit.")
            inky_display.wait_for_window_close()
        else:
            self.print_display(inky_display)

    def print_console(self):
        pass

    def print_display(self, inky_display):
        pass

    def _get_inky(self):
        if self._display_mode == DisplayMode.NO:
            return None

        if self._display_mode == DisplayMode.MOCK:
            return InkyMockPHAT(self._colour)
        else:
            return InkyPHAT(self._colour)
