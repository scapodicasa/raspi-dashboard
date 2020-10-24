import spotify as sp

import asyncio
import datetime

import logging

log_level = logging.INFO

logging.basicConfig(level=log_level)

spotify = sp.SpotifyService()

async def main():

    current = None

    while True:
        result = spotify.currently_playing()

        if result.current_playing is not None:
            if current is None or (current is not None and current.timestamp < result.current_playing.timestamp and not result.is_same_track(current)):
                current = result.current_playing
                logging.info(result)
        else:
            logging.info("Spotify not playing.")

        await asyncio.sleep(5)

asyncio.run(main())
