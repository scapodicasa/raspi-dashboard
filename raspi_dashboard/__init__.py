import asyncio

import time

from .spotify import SpotifyService
from .clock import ClockService

import logging
log_level = logging.INFO
logging.basicConfig(
    level=log_level, format='[%(levelname)s] %(asctime)s [%(name)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

spotify = SpotifyService()
clock = ClockService(lambda: logging.info(time.strftime("%H:%M")))

spotify_stopped = False


async def main():
    global spotify_stopped

    current_spotify = None

    while True:
        spotify_result = None
        try:
            spotify_result = spotify.currently_playing()
        except Exception as ex:
            logging.exception(ex)

        if spotify_result.current_playing is not None:
            spotify_stopped = False

            if clock.is_running():
                clock.stop()

            if current_spotify is None or (current_spotify.current_playing is not None and spotify_result != current_spotify):
                current_spotify = spotify_result
                logging.info(spotify_result)
        else:
            current_spotify = None
            if not spotify_stopped:
                spotify_stopped = True
                clock.start()

        await asyncio.sleep(5)


def start():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logging.info("Stopping.")
    finally:
        loop.close()
        logging.info("Stopped.")
