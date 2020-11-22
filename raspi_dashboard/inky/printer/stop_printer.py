from PIL import Image, ImageFont, ImageDraw
from font_intuitive import Intuitive

from .printer_base import PrinterBase

import logging
logger = logging.getLogger(__name__)


class StopPrinter(PrinterBase):
    _message = "raspi\n\t\tdashboard"

    def get_console_text(self):
        return self._message

    def get_display_img(self, inky_display):
        scale_size = 1

        img = Image.new(
            "P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.BLACK)
        draw = ImageDraw.Draw(img)

        intuitive_font = ImageFont.truetype(Intuitive, int(45 * scale_size))

        w, h = intuitive_font.getsize_multiline(self._message)
        x = int((inky_display.WIDTH - w) / 2)
        y = int((inky_display.HEIGHT - h) / 2)
        draw.multiline_text((x, y), self._message,
                            inky_display.WHITE, font=intuitive_font)

        return img
