import argparse
import asyncio
import atexit
import time

from .core.config import initialize_config
from .core.services import ClockService, SpotifyService, ServiceBase
from .inky import DisplayMode
from .inky.printer import ClockPrinter, SpotifyPrinter, StopPrinter

import logging
log_level = logging.INFO
logging.basicConfig(
    level=log_level, format='[%(levelname)s] %(asctime)s [%(name)s]: %(message)s', datefmt='%d/%m/%Y %H:%M:%S')

logger = logging.getLogger(__name__)


def parse_main_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--display", choices=[mode.value for mode in DisplayMode], help="Use this program without an Inky display.")
    return parser.parse_args()


def stop_print(args):
    StopPrinter(args.display).print()


def main():
    args = parse_main_args()

    atexit.register(lambda: stop_print(args))

    spotify = initialize_spotify()
    if spotify is None:
        logger.error("Spotify not initializated. Exiting.")
        return

    spotify.register(SpotifyService.Events.ON_STOP_PLAYING,
                     lambda: clock.start())

    def handle_spotify_start_playing(track):
        SpotifyPrinter(args.display, track).print()
        clock.stop()

    spotify.register(SpotifyService.Events.ON_START_PLAYING,
                     handle_spotify_start_playing)
    spotify.register(SpotifyService.Events.ON_TRACK_CHANGE,
                     lambda track: SpotifyPrinter(args.display, track).print())

    clock_printer = ClockPrinter(args.display)
    clock = ClockService()
    clock.register(ServiceBase.Events.ON_TRIGGER,
                   lambda: clock_printer.print())

    clock.start()
    spotify.start()


def start():
    logger.info("Starting.")
    loop = asyncio.get_event_loop()
    try:
        main()
        loop.run_forever()
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
