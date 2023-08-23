import aiogram
from spotipy.client import Spotify
import message_handler.track_checking


async def msg_handler(message: aiogram.types.Message):
    funcs = [track_checking.message_handler]

    for func in funcs:
        await func(message)


def setup(dp: aiogram.Dispatcher, spoty_client: Spotify):
    message_handler.track_checking.spotify_client = spoty_client

    dp.register_message_handler(msg_handler, content_types=['text'])
