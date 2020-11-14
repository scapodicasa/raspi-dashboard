import time

from PIL import Image, ImageFont, ImageDraw
from font_intuitive import Intuitive

from .printer_base import PrinterBase

import logging
logger = logging.getLogger(__name__)


class ClockPrinter(PrinterBase):

    def get_console_text(self):
        logger.debug("get_console_text")

        return time.strftime("%H:%M")

    def get_display_img(self, inky_display):
        logger.debug("get_display_img")

        now = time.strftime("%H:%M")

        scale_size = 1

        inky_display.set_border(self._colour)

        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(Intuitive, int(84 * scale_size))

        for y in range(0, inky_display.HEIGHT):
            for x in range(0, inky_display.WIDTH):
                img.putpixel((x, y), inky_display.BLACK)

        name_w, name_h = font.getsize(now)
        name_x = int((inky_display.WIDTH - name_w) / 2)
        name_y = int((inky_display.HEIGHT - name_h) / 2)
        draw.text((name_x, name_y), now, inky_display.WHITE, font=font)

        return img
