from os.path import expanduser, join

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ..config import LOCAL_DATA_DIR, CONFIG

from .model import SpotifyUser, SpotifyCurrentPlaying, SpotifyPlaylist, SpotifyPlayingInfo

import logging
logger = logging.getLogger(__name__)


class SpotifyService:

    spotify = None

    def __init__(self):
        logger.info("Initializing Spotify service.")

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CONFIG['SPOTIFY']['CLIENT_ID'],
                                                                 client_secret=CONFIG['SPOTIFY']['CLIENT_SECRET'],
                                                                 redirect_uri="http://localhost",
                                                                 open_browser=False,
                                                                 scope="user-library-read user-read-playback-state",
                                                                 cache_path=join(LOCAL_DATA_DIR, "spotify-cache")))

    def user(self):
        try:
            us = self.spotify.me()
            return SpotifyUser(**us)
        except Exception as ex:
            logger.info("Spotify remote call failed.")
            logger.debug(ex)
            return None

    def currently_playing(self):
        cp = None
        try:
            cp = self.spotify.currently_playing(additional_types='episode')
        except Exception as ex:
            logger.info("Spotify remote call failed.")
            logger.debug(ex)
            return SpotifyPlayingInfo()

        if cp is not None:
            current_playing = SpotifyCurrentPlaying(**cp)
            logger.debug(f"Current: {current_playing}")

            if current_playing.is_playing:
                playlist = None
                if current_playing.context is not None and current_playing.context.type == 'playlist':
                    pl = self.spotify.playlist(
                        current_playing.context.type_id, fields='id,uri,name,description')
                    playlist = SpotifyPlaylist(**pl)
                    logger.debug(f"Playlist: {playlist}")
                else:
                    logger.debug("Context is not playlist.")

                return SpotifyPlayingInfo(current_playing=current_playing, playlist=playlist)
            else:
                logger.debug(
                    "Got playing info from Spotify, but it's not playing.")
                return SpotifyPlayingInfo()
        else:
            logger.debug("Playing info was not provided from Spotify.")
            return SpotifyPlayingInfo()
