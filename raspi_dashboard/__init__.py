from .spotify import SpotifyService
from .clock import ClockService

import asyncio

import time

import logging
log_level = logging.INFO
logging.basicConfig(
    level=log_level, format='[%(levelname)s] %(asctime)s [%(name)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

spotify = SpotifyService()
clock = ClockService(lambda: logging.info(time.strftime("%H:%M")))

spotify_stopped = False


async def main():
    global spotify_stopped

    current = None

    while True:
        try:
            result = spotify.currently_playing()

            if result.current_playing is not None:
                spotify_stopped = False

                if clock.is_running():
                    clock.stop()

                if current is None or (current.current_playing is not None and result != current):
                    current = result
                    logging.info(result)
            else:
                current = None
                if not spotify_stopped:
                    spotify_stopped = True
                    clock.start()


        except Exception as ex:
            logging.exception(ex)

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
