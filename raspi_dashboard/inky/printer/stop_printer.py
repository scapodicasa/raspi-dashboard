from PIL import Image, ImageFont, ImageDraw
from font_intuitive import Intuitive

from .printer_base import PrinterBase

import logging
logger = logging.getLogger(__name__)


class StopPrinter(PrinterBase):
    _message = "raspi\n\t\tdashboard"

    def get_console_text(self):
        logger.debug("get_console_text")

        return self._message

    def get_display_img(self, inky_display):
        logger.debug("get_display_img")

        scale_size = 1

        inky_display.set_border(inky_display.RED)

        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)

        intuitive_font = ImageFont.truetype(Intuitive, int(45 * scale_size))

        for y in range(0, inky_display.HEIGHT):
            for x in range(0, inky_display.WIDTH):
                img.putpixel((x, y), inky_display.BLACK)

        w, h = intuitive_font.getsize_multiline(self._message)
        x = int((inky_display.WIDTH - w) / 2)
        y = int((inky_display.HEIGHT - h) / 2)
        draw.multiline_text((x, y), self._message,
                            inky_display.WHITE, font=intuitive_font)

        return img
