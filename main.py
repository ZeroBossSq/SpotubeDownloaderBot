from string import ascii_letters
from os import remove

import pytube
import telebot

from Track.track import SpotiClient

bot = telebot.TeleBot('5796112493:AAFlNo1Zy63DDa1PilW3nUwu8kNDm7-4vdk')

s_client = SpotiClient(client_id='114f74f9e39642088f38dd2ff019c55b',
                       client_secret='fef5e90b9bb743a392e109a7d0fc5934')


def justify_track_fname(track_full_name: str):
    return ''.join([i for i in list(track_full_name) if i in ascii_letters])


@bot.message_handler()
def msg_handler(msg: telebot.types.Message):
    track_name = ''
    founded = False

    if 'spotify' in msg.text:
        track = s_client.get_track(msg.text)

        # bot.send_message(msg.chat.id, '')
        bot.send_photo(msg.chat.id, photo=track.album_imgs.medium.bytes,
                       caption=f'`{track.full_name}` ({track.duration} min) (Images: '
                               f'[Large]({track.album_imgs.large.url}), [Medium]({track.album_imgs.medium.url}), [Small]({track.album_imgs.small.url}))',
                       parse_mode='MARKDOWN')

        track_name = track.full_name
        founded = True
    elif 'youtu' in msg.text:
        track = pytube.YouTube(msg.text)
        track_name = f'{track.title} - {track.author}'

        bot.send_photo(msg.chat.id, track.thumbnail_url, track_name)
        founded = True

    if founded:
        message = bot.send_message(msg.chat.id, text='Searching')
        download_track: pytube.YouTube = pytube.Search(track_name).results[0]

        bot.edit_message_text('Downloading', msg.chat.id, message.id)
        download_track.streams.get_audio_only().download(filename=f'{justify_track_fname(track_name)}.mp3')

        bot.edit_message_text('Sending', msg.chat.id, message.id)
        track_bytes = open(f'{justify_track_fname(track_name)}.mp3', 'rb').read()

        bot.send_audio(msg.chat.id, audio=track_bytes, title=track_name)
        bot.edit_message_text('Done', msg.chat.id, message.id)

        remove(justify_track_fname(track_name))
    else:
        bot.send_message(msg.chat.id, text="Your search query doesn't found")


print(f'@{bot.get_me().username} | {bot.get_me().full_name} [{bot.get_me().id}]')

bot.skip_pending = True
bot.polling(none_stop=True)
