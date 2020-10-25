from .spotify import SpotifyService

import asyncio
import datetime

import logging

log_level = logging.INFO

logging.basicConfig(level=log_level)

spotify = SpotifyService()


async def main():

    current = None

    while True:
        result = spotify.currently_playing()

        if result.current_playing is not None:
            if current is None or (current.current_playing is not None and result != current):
                current = result
                logging.info(result)
        else:
            logging.info("Spotify not playing.")

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
