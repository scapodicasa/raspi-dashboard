import asyncio
import time

from .config import initialize_config

from .clock import ClockService
from .spotify import SpotifyService
from .inky import print_clock, print_spotify

import logging
log_level = logging.INFO
logging.basicConfig(
    level=log_level, format='[%(levelname)s] %(asctime)s [%(name)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

logger = logging.getLogger(__name__)


async def main():
    spotify = initialize_spotify()
    if spotify is None:
        logger.error("Spotify not initializated. Exiting.")
        return

    clock = ClockService(print_clock)

    spotify_stopped = False
    current_spotify = None

    while True:
        spotify_result = spotify.currently_playing()

        if spotify_result is not None and spotify_result.current_playing is not None:
            spotify_stopped = False

            if clock.is_running():
                clock.stop()

            if current_spotify is None or (current_spotify.current_playing is not None and spotify_result != current_spotify):
                current_spotify = spotify_result
                print_spotify(spotify_result)
        else:
            current_spotify = None
            if not spotify_stopped:
                spotify_stopped = True
                clock.start()

        await asyncio.sleep(5)


def start():
    logger.info("Starting.")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        logger.info("Stopping.")
    finally:
        loop.close()
        logger.info("Stopped.")


def initialize():
    try:
        initialize_config()
        initialize_spotify()
    except KeyboardInterrupt:
        pass


def initialize_spotify():
    spotify = None
    try:
        spotify = SpotifyService()
        user = spotify.user()

        if user is not None:
            logger.info(f"Logged as: {user.display_name} a.k.a. {user.id}")
        else:
            logger.error("Spotify login failed.")

    except Exception as ex:
        logger.debug(ex)
        logger.error("Spotify initialization failed.")

    return spotify
