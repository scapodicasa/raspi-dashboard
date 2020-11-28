from threading import Thread, Lock

from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT, InkyMockPHAT

from font_intuitive import Intuitive

from .. import DisplayMode
from ...core.config import CONFIG

import logging
logger = logging.getLogger(__name__)


class PrinterBase:
    _display_mode = None
    _flip = None

    _colour = None

    _lock = Lock()

    _default_message = "raspi\n\t\tdashboard"

    def __init__(self, display_mode):
        self._display_mode = DisplayMode(
            display_mode) if display_mode is not None else None

        self._flip = CONFIG.getboolean("INKY", "flip")
        self._colour = CONFIG['INKY']['colour']

    def print(self):
        console_text = self.get_console_text()
        logger.info(console_text)

        if self._display_mode == DisplayMode.NO:
            return

        inky_display = self._get_inky()

        border_colour = inky_display.BLACK
        if self._colour == 'red':
            border_colour = inky_display.RED
        elif self._colour == 'yellow':
            border_colour = inky_display.YELLOW

        inky_display.set_border(border_colour)

        if self._display_mode != DisplayMode.NO:
            img = self.get_display_img(inky_display)

            if img is None:
                img = PrinterBase.get_default_image(inky_display)
                logger.warning(
                    "Image not correctly created. Showing default image.")

            if self._flip:
                img = img.rotate(180)

            inky_display.set_image(img)

        if self._display_mode == DisplayMode.MOCK:
            logger.info("Press Ctrl+C or close window to exit.")
            inky_display.show()
            inky_display.wait_for_window_close()
        else:
            def show():
                with self._lock:
                    inky_display.show()

            Thread(target=show).start()

    def get_console_text(self):
        return self._default_message

    def get_display_img(self, inky_display):
        return PrinterBase.get_default_image(inky_display)

    @classmethod
    def get_default_image(self, inky_display):
        scale_size = 1

        img = Image.new(
            "P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.BLACK)
        draw = ImageDraw.Draw(img)

        intuitive_font = ImageFont.truetype(Intuitive, int(45 * scale_size))

        w, h = intuitive_font.getsize_multiline(self._default_message)
        x = int((inky_display.WIDTH - w) / 2)
        y = int((inky_display.HEIGHT - h) / 2)
        draw.multiline_text((x, y), self._default_message,
                            inky_display.WHITE, font=intuitive_font)

        return img

    def _get_inky(self):
        if self._display_mode == DisplayMode.NO:
            return None

        if self._display_mode == DisplayMode.MOCK:
            return InkyMockPHAT(self._colour)
        else:
            return InkyPHAT(self._colour)
