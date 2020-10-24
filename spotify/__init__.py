import json
import asyncio
from datetime import datetime, date

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from secrets import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

class SpotifyService:

    spotify = None

    def __init__(self):
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                                                 client_secret=SPOTIFY_CLIENT_SECRET,
                                                                 redirect_uri="http://localhost",
                                                                 open_browser=False,
                                                                 scope="user-library-read user-read-playback-state"))

    def user(self):
        return SpotifyUser(**self.spotify.me())

    def currently_playing(self):
        return SpotifyCurrentPlaying(**self.spotify.currently_playing())

    async def currently_playing_after_delay(self, delay):
        await asyncio.sleep(delay)
        return self.currently_playing()


class SpotifyModel:
    def todict(self, obj, classkey=None):
        if isinstance(obj, dict):
            data = {}
            for (k, v) in obj.items():
                data[k] = self.todict(v, classkey)
            return data
        elif hasattr(obj, "_ast"):
            return self.todict(obj._ast())
        elif hasattr(obj, "__iter__") and not isinstance(obj, str):
            return [self.todict(v, classkey) for v in obj]
        elif hasattr(obj, "__dict__"):
            data = dict([(key, self.todict(value, classkey))
                         for key, value in obj.__dict__.items()
                         if not callable(value) and not key.startswith('_')])
            if classkey is not None and hasattr(obj, "__class__"):
                data[classkey] = obj.__class__.__name__
            return data
        else:
            return obj

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    def __repr__(self):
        return json.dumps(self.todict(self), default=self.json_serial)


class SpotifyUser(SpotifyModel):

    display_name = None
    id = None

    def __init__(self, display_name=None, id=None, **kwargs):
        self.display_name = display_name
        self.id = id


class SpotifyCurrentPlaying(SpotifyModel):

    timestamp = None
    item = None

    def __init__(self, timestamp=None, item=None, **kwargs):
        self.timestamp = datetime.fromtimestamp(timestamp/1000)
        self.item = SpotifyCurrentPlayingItem(type_=item['type'], **item)

    def is_same_track(self, other):
        return (self.item.name == other.item.name and self.item.album.name == other.item.album.name)


class SpotifyCurrentPlayingItem(SpotifyModel):

    type = None
    name = None
    album = None
    artists = None

    def __init__(self, type_=None, name=None, album=None, artists=None, **kwargs):
        self.type = type_
        self.name = name
        self.album = SpotifyCurrentPlayingItemAlbum(**album)
        self.artists = [SpotifyArtist(**a) for a in artists]


class SpotifyCurrentPlayingItemAlbum(SpotifyModel):

    name = None
    images = None

    def __init__(self, name=None, images=None, **kwargs):
        self.name = name
        self.images = [
            SpotifyCurrentPlayingItemAlbumImage(**i) for i in images]


class SpotifyCurrentPlayingItemAlbumImage(SpotifyModel):

    height = None
    width = None
    url = None

    def __init__(self, height=None, width=None, url=None, **kwargs):
        self.height = height
        self.width = width
        self.url = url


class SpotifyArtist(SpotifyModel):

    name = None

    def __init__(self, name=None, **kwargs):
        self.name = name
