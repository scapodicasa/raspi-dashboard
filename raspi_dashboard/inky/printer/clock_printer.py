import time

from PIL import Image, ImageFont, ImageDraw
from font_intuitive import Intuitive

from .printer_base import PrinterBase

import logging
logger = logging.getLogger(__name__)


class ClockPrinter(PrinterBase):

    def get_console_text(self):
        return time.strftime("%H:%M")

    def get_display_img(self, inky_display):
        now = time.strftime("%H:%M")

        scale_size = 1

        img = Image.new(
            "P", (inky_display.WIDTH, inky_display.HEIGHT), inky_display.BLACK)
        draw = ImageDraw.Draw(img)

        font = ImageFont.truetype(Intuitive, int(84 * scale_size))

        w, h = font.getsize(now)
        x = int((inky_display.WIDTH - w) / 2)
        y = int((inky_display.HEIGHT - h) / 2)
        draw.text((x, y), now, inky_display.WHITE, font=font)

        return img
