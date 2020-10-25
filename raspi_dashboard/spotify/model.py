from datetime import date, datetime
import json

import logging
logger = logging.getLogger(__name__)


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


class SpotifyPlayingInfo(SpotifyModel):
    current_playing = None
    playlist = None

    def __init__(self, current_playing=None, playlist=None):
        self.current_playing = current_playing
        self.playlist = playlist

    def __eq__(self, other):
        if self.current_playing.context.uri != other.current_playing.context.uri:
            return False

        if self.current_playing.item.id != other.current_playing.item.id:
            return False

        if self.playlist is not None:
            if other.playlist is None:
                logger.debug("is_same_track: False.")
                return False
            else:
                if self.playlist.id != other.playlist.id:
                    logger.debug("is_same_track: False.")
                    return False
        else:
            if other.playlist is not None:
                logger.debug("is_same_track: False.")
                return False

        logger.debug("is_same_track: True.")
        return True

    def __ne__(self, other):
        return not self.__eq__(other)


class SpotifyCurrentPlaying(SpotifyModel):

    timestamp = None
    context = None
    progress = None
    item = None
    is_playing = None

    progress_percentage = None

    def __init__(self, timestamp=None, context=None, progress_ms=None, item=None, is_playing=None, **kwargs):
        self.timestamp = datetime.fromtimestamp(timestamp/1000)
        self.progress = progress_ms

        if context is not None:
            self.context = SpotifyCurrentPlayingContext(
                type_=context['type'], **context)

        if item is not None:
            self.item = SpotifyCurrentPlayingItem(type_=item['type'], **item)

            self.progress_percentage = round(
                self.progress / self.item.duration * 100, 2)

        self.is_playing = is_playing


class SpotifyCurrentPlayingContext(SpotifyModel):

    type = None
    uri = None

    type_id = None

    def __init__(self, type_=None, uri=None, **kwargs):
        self.type = type_
        self.uri = uri

        self.type_id = uri.split(':')[-1]


class SpotifyCurrentPlayingItem(SpotifyModel):
    id = None
    duration = None
    type = None
    name = None
    album = None
    show = None
    artists = None

    def __init__(self, id=None, duration_ms=None, type_=None, name=None, album=None, show=None, artists=None, **kwargs):
        self.id = id
        self.duration = duration_ms
        self.type = type_
        self.name = name

        if album is not None:
            self.album = SpotifyCurrentPlayingItemAlbum(**album)

        if show is not None:
            self.show = SpotifyCurrentPlayingItemShow(**show)

        if artists is not None:
            self.artists = [SpotifyArtist(**a) for a in artists]


class SpotifyCurrentPlayingItemAlbum(SpotifyModel):

    name = None
    images = None

    def __init__(self, name=None, images=None, **kwargs):
        self.name = name
        self.images = [
            SpotifyCurrentPlayingItemAlbumImage(**i) for i in images]


class SpotifyCurrentPlayingItemShow(SpotifyModel):

    description = None
    name = None
    images = None
    publisher = None

    def __init__(self, description=None, name=None, images=None, publisher=None, **kwargs):
        self.description = description
        self.name = name
        self.images = [
            SpotifyCurrentPlayingItemAlbumImage(**i) for i in images]
        self.publisher = publisher


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


class SpotifyPlaylist(SpotifyModel):

    id = None
    uri = None
    name = None
    description = None

    def __init__(self, id=None, uri=None, name=None, description=None, **kwargs):
        self.id = id
        self.uri = uri
        self.name = name
        self.description = description
