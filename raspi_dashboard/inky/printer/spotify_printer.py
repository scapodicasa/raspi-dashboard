from io import BytesIO
import requests
import numpy as np

from PIL import Image, ImageFont, ImageDraw

from font_roboto import Roboto

from .printer_base import PrinterBase

import logging
logger = logging.getLogger(__name__)


class SpotifyPrinter(PrinterBase):
    _result = None

    _margin = 7

    def __init__(self, display_mode, result):
        super().__init__(display_mode)
        self._result = result

    def print_console(self):
        logger.info(self._result)

    def print_display(self, inky_display):
        result = self._result

        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))

        try:
            album = result.current_playing.item.show if result.current_playing.item.show is not None else result.current_playing.item.album
            album_images = [i for i in album.images if i.height == 64]
            image_found = False

            if len(album_images) > 0:
                image_found = True
                album_image = album_images[0]

                try:
                    response = requests.get(album_image.url)

                    if response.status_code == 200:
                        cover = Image.open(BytesIO(response.content))
                        cover.convert("1")
                        cover = np.asarray(cover)

                        bw = []

                        for x in cover:
                            row = []
                            bw.append(row)
                            for y in x:
                                row.append(sum(y) / len(y))
                    else:
                        logger.info(
                            f"Error downloading image from: {album_image.url}.")
                except Exception as ex:
                    logger.info(
                        f"Error downloading image from: {album_image.url}.")
                    logger.debug(ex)

            else:
                logger.info("Image with height of 64 px not found.")

            if image_found:
                a = inky_display.HEIGHT / 2
                b = len(bw) / 2
                c = self._margin + len(bw[0])

            for y in range(0, inky_display.HEIGHT):
                for x in range(0, inky_display.WIDTH):
                    color = inky_display.BLACK
                    if image_found:
                        if y >= a - b and y < a + b:
                            if x >= self._margin and x < c:
                                if bw[int(y - (a - b))][int(x - self._margin)] > 128:
                                    color = inky_display.WHITE

                    img.putpixel((x, y), color)

            font = ImageFont.truetype(Roboto, size=12)

            opera = result.current_playing.item.show.name if result.current_playing.item.show is not None else result.current_playing.item.album.name

            artist = result.current_playing.item.show.publisher if result.current_playing.item.show is not None else ",".join(
                [a.name for a in result.current_playing.item.artists])

            msg = f"""T: {result.current_playing.item.name}
O: {opera}       
A: {artist}"""

            w, h = font.getsize_multiline(msg)
            w = 7 + (7 + album_image.width if image_found else 0)
            h = int((inky_display.HEIGHT - h) / 2)

            draw = ImageDraw.Draw(img)

            draw.multiline_text((w, h), msg, inky_display.WHITE, font=font)

            playing_on = f"D: {result.current_playing.device.name}"

            w, h = font.getsize(playing_on)
            x = int((inky_display.WIDTH - w - self._margin))
            y = int(inky_display.HEIGHT - h - self._margin)
            draw.text((x, y), playing_on, inky_display.WHITE, font=font)

            inky_display.set_border(self._colour)

            inky_display.set_image(img)
            inky_display.show()

        except Exception as ex:
            logger.info("Unexpected exception happened.")
            logger.debug(ex)
