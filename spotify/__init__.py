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

        cp = self.spotify.currently_playing(additional_types='episode')

        if cp is not None:
            current_playing = SpotifyCurrentPlaying(**cp)
            logger.debug(f"Current: {current_playing}")

            if current_playing.is_playing:
                playlist = None
                if current_playing.context.type == 'playlist':
                    pl = self.spotify.playlist(current_playing.context.type_id)
                    playlist = SpotifyPlaylist(**pl)

                return SpotifyPlayingInfo(current_playing=current_playing, playlist=playlist)
            else:
                logger.debug(
                    "Got playing info from Spotify, but it's not playing. Returning None.")
                return SpotifyPlayingInfo()
        else:
            logger.debug(
                "Playing info was not provided from Spotify. Returning None.")
            return SpotifyPlayingInfo()
