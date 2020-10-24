import spotify as sp

import asyncio
import datetime

spotify = sp.SpotifyService()


async def main():

    current = None

    while True:
        result = spotify.currently_playing()

        if result is not None:
            if current is None or (current is not None and current.timestamp < result.timestamp and not result.is_same_track(current)):
                current = result
                print(current)
        else:
            print("Spotify not playing.")

        await asyncio.sleep(5)


asyncio.run(main())
