from urllib.request import urlopen
from spotipy.client import Spotify


class SpotifyTrackInfo:
    def __init__(self, spotify_client: Spotify, url: str):
        self.url = url

        track: dict = spotify_client.track(self.url)
        album_images = [i.get('url') for i in track.get('album').get('images')]

        self.name = track.get('name')
        self.album_images = SpotifyTrackImages(url_small=album_images[2],
                                               url_medium=album_images[1],
                                               url_large=album_images[0])
        self.artists = [i.get('name') for i in track.get('artists')]
        self.duration = round(float(track["duration_ms"]) / 1000 / 60, 1)  # round to 1 num after .
        self.full_name = f'{self.name} - {", ".join(self.artists)}'


class SpotifyTrackImages:
    def __init__(self, url_large: str, url_medium: str, url_small: str):
        self.large = SpotifyTrackImage(url=url_large)
        self.medium = SpotifyTrackImage(url=url_medium)
        self.small = SpotifyTrackImage(url=url_small)


class SpotifyTrackImage:
    def __init__(self, url: str):
        self.url = url
        self.bytes: bytes = urlopen(url).read()
