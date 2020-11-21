from os.path import expanduser, join
from datetime import datetime, timedelta
from enum import Enum

from apscheduler.triggers.date import DateTrigger

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from ...publisher import Publisher
from ...config import LOCAL_DATA_DIR, CONFIG
from .. import ServiceBase
from .model import SpotifyUser, SpotifyCurrentPlaying, SpotifyPlaylist, SpotifyPlayingInfo

import logging
logging.getLogger(spotipy.__name__).setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class SpotifyService(ServiceBase):

    spotify = None
    current = None

    class Events(Enum):
        ON_START_PLAYING = 'on_start_playing'
        ON_STOP_PLAYING = 'on_stop_playing'
        ON_TRACK_CHANGE = 'on_track_change'

    def __init__(self):

        Publisher.__init__(self, events=(
            [mode for mode in SpotifyService.Events] + [mode for mode in ServiceBase.Events]))

        self._internal_init()

        self.register(ServiceBase.Events.ON_TRIGGER, self.currently_playing)

        logger.info("Initializing Spotify service.")

        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CONFIG['SPOTIFY']['client_id'],
                                                                 client_secret=CONFIG['SPOTIFY']['client_secret'],
                                                                 redirect_uri=CONFIG['SPOTIFY']['redirect_uri'],
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

    def get_next_trigger(self):
        now = datetime.now()
        now = now + timedelta(seconds=5)
        trigger = DateTrigger(
            datetime(now.year, now.month, now.day, now.hour, now.minute, now.second))

        logger.info(f"Returng trigger: {trigger}")

        return trigger

    def currently_playing(self):
        new_playing = None

        call_result = None
        try:
            call_result = self.spotify.current_playback(
                additional_types='episode')
        except Exception as ex:
            logger.info("Spotify remote call failed.")
            logger.debug(ex)

        if call_result is not None:
            current_playing = SpotifyCurrentPlaying(**call_result)
            logger.debug(f"Current: {current_playing}")

            if current_playing.is_playing:
                playlist = None
                if current_playing.context is not None and current_playing.context.type == 'playlist':
                    try:
                        pl = self.spotify.playlist(
                            current_playing.context.type_id, fields='id,uri,name,description')
                        playlist = SpotifyPlaylist(**pl)
                        logger.debug(f"Playlist: {playlist}")
                    except Exception as ex:
                        logger.info("Spotify playlist call failed.")
                        logger.debug(ex)
                        playlist = SpotifyPlaylist(name="Unknown")
                else:
                    logger.debug("Context is not playlist.")

                new_playing = SpotifyPlayingInfo(
                    current_playing=current_playing, playlist=playlist)

            else:
                logger.debug(
                    "Got playing info from Spotify, but it's not playing.")
        else:
            logger.debug("Playing info was not provided from Spotify.")

        if self.current is not None and new_playing is not None:
            if self.current != new_playing:
                logger.info(f"Firing event: {self.Events.ON_TRACK_CHANGE}")
                self.dispatch(self.Events.ON_TRACK_CHANGE, new_playing)

        elif self.current is not None and new_playing is None:
            logger.info(f"Firing event: {self.Events.ON_STOP_PLAYING}")
            self.dispatch(self.Events.ON_STOP_PLAYING)

        elif self.current is None and new_playing is not None:
            logger.info(f"Firing event: {self.Events.ON_START_PLAYING}")
            self.dispatch(self.Events.ON_START_PLAYING, new_playing)

        self.current = new_playing
