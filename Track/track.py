from urllib.request import urlopen
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


class SpotiClient:
    def __init__(self, client_id: str, client_secret: str):
        self.credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.spotify_client = Spotify(auth_manager=self.credentials)

    def get_track(self, url: str):
        return SpotiTrack(spotify_client=self.spotify_client, url=url)


class SpotiTrack:
    def __init__(self, spotify_client: Spotify, url: str):
        self.url = url

        track: dict = spotify_client.track(self.url)
        alb_imgs = [i.get('url') for i in track.get('album').get('images')]

        self.name = track.get('name')
        self.album_imgs = SpotifyTrackImages(url_small=alb_imgs[2],
                                             url_medium=alb_imgs[1],
                                             url_large=alb_imgs[0])
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
