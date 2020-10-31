import time

from PIL import Image, ImageFont, ImageDraw
from inky import InkyMockPHAT as InkyPHAT
from font_intuitive import Intuitive

from ..config import CONFIG

import logging
logger = logging.getLogger(__name__)


def print(without_display=False):
    now = time.strftime("%H:%M")
    logger.info(now)

    if without_display:
        return

    colour = CONFIG['INKY']['colour']

    inky_display = InkyPHAT(colour)
    scale_size = 1

    inky_display.set_border(inky_display.RED)

    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    intuitive_font = ImageFont.truetype(Intuitive, int(84 * scale_size))

    for y in range(0, inky_display.HEIGHT):
        for x in range(0, inky_display.WIDTH):
            img.putpixel((x, y), inky_display.BLACK)

    name_w, name_h = intuitive_font.getsize(now)
    name_x = int((inky_display.WIDTH - name_w) / 2)
    name_y = int((inky_display.HEIGHT - name_h) / 2)
    draw.text((name_x, name_y), now, inky_display.WHITE, font=intuitive_font)

    # Display the completed name badge

    inky_display.set_image(img)
    inky_display.show()

    logger.info("Press Ctrl+C or close window to exit...")
    inky_display.wait_for_window_close()
