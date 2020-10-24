import logging

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

from .model import *

logger = logging.getLogger(__name__)


class SpotifyService:

    spotify = None

    def __init__(self):
        logger.info("Initializing Spotify service.")

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                                 client_secret=SPOTIFY_CLIENT_SECRET,
                                                                 redirect_uri="http://localhost",
                                                                 open_browser=False,
                                                                 scope="user-library-read user-read-playback-state"))

    def user(self):
        return SpotifyUser(**self.spotify.me())

    def currently_playing(self):
        result = self.spotify.currently_playing()

        if result is not None:
            current = SpotifyCurrentPlaying(**result)
            logger.debug(f"Current: {current}")

            if current.is_playing:
                return current
            else:
                logger.debug(
                    "Got playing info from Spotify, but it's not playing. Returning None.")
                return None
        else:
            logger.debug(
                "Playing info was not provided from Spotify. Returning None.")
            return None
