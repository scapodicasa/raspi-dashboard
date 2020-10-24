import spotify as sp

import asyncio
import datetime

spotify = sp.SpotifyService()

async def main():

    current = spotify.currently_playing()
    print(current)
    result = current
    while True:
        if current.timestamp < result.timestamp and not result.is_same_track(current):
            current = result
            print(current)
        result = await spotify.currently_playing_after_delay(5)


asyncio.run(main())

