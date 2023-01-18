from string import ascii_letters
from datetime import datetime
from os import remove
import json
import requests

import pytube
import telebot

import env
from Track.track import SpotiClient
from backgrounds import start_keeping
# from database import db

start_keeping()


class Audio:
    def __init__(self, audio_bytes: bytes, thumb: bytes):
        self.audio_bytes = audio_bytes
        self.thumb = thumb


bot = telebot.TeleBot(env.TELEGRAM_BOT_TOKEN)
s_client = SpotiClient(client_id=env.SPOTIPY_CLIENT_ID, client_secret=env.SPOTIPY_CLIENT_TOKEN)
start_markup = telebot.types.InlineKeyboardMarkup(row_width=2)
start_markup.add(
    telebot.types.InlineKeyboardButton('Donate 💎', callback_data='donate'),
    telebot.types.InlineKeyboardButton('Support 🧰', url='https://t.me/ZXBTLKXC')
)

try:
    db: dict = json.load(open('db.json'))
except BaseException:
    with open('db.json', 'w') as file:
        file.write('{}')
    db = {}


def justify_track_fname(track_full_name: str):
    return ''.join([i for i in list(track_full_name) if i in ascii_letters])


# def add_file_id_to_mysql(track_full_name: str, file_id: str):
#     connection = db.get_connection()
#     cursor = connection.cursor(dictionary=True)
#
#     cursor.execute(f"INSERT INTO downloader (track_full_name, file_id) VALUES ('{track_full_name}, {file_id})")
#     connection.commit()
#
#
# def get_audio_by_file_id():
#     ...


def get_bytes_by_url(url: str) -> bytes:
    return requests.get(url).content


def add_file_id_to_json(track_full_name: str, file_id: str, thumb_url: str):
    db[track_full_name] = f'{file_id}||{thumb_url}'
    json.dump(db, open('db.json', 'w'))


def get_audio_by_full_name(track_full_name: str) -> Audio | None:
    try:
        audio_url, thumb_url = db[track_full_name].split('||')
        url = bot.get_file_url(audio_url)

        return Audio(get_bytes_by_url(url), get_bytes_by_url(thumb_url))
    except KeyError:
        return None


@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    bot.send_message(msg.chat.id, "Hi! 👋\n"
                                  "I'm a bot 🤖 downloads music from spotify 🎧 and youtube 🎬 that's under 5️⃣ minutes long!\n"
                                  "Just send me link to the track and I'll download it for you! ✨", reply_markup=start_markup)


@bot.message_handler()
def msg_handler(msg: telebot.types.Message):
    # "triggered" var = protection against random messages not related to the track
    try:
        track_name, track, founded, triggered = '', None, False, False

        if 'spotify' in msg.text:
            bot.send_message(msg.chat.id, '⏳')

            track = s_client.get_track(msg.text)

            bot.send_photo(msg.chat.id, photo=track.album_imgs.large.bytes,
                           caption=f'`{track.full_name}` ({track.duration} min) (Images: '
                                   f'[Large]({track.album_imgs.large.url}), [Medium]({track.album_imgs.medium.url}), [Small]({track.album_imgs.small.url}))',
                           parse_mode='MARKDOWN')

            track_name = track.full_name
            founded, triggered = True, True
        elif 'youtu' in msg.text:
            bot.send_message(msg.chat.id, '⏳')

            track = pytube.YouTube(msg.text)
            track_name = f'{track.title} - {track.author}'

            bot.send_photo(msg.chat.id, track.thumbnail_url, track_name)
            founded, triggered = True, True

        if founded:
            message = bot.send_message(msg.chat.id, text='Searching 🔍')

            track_bytes = get_audio_by_full_name(track_name)
            if track_bytes is not None:
                bot.edit_message_text('Sending ⚙️', msg.chat.id, message.id)
                bot.send_audio(msg.chat.id, audio=track_bytes.audio_bytes, title=track_name, thumb=track_bytes.thumb)
                bot.edit_message_text('Done ✅', msg.chat.id, message.id)

                return None

            download_track: pytube.YouTube = pytube.Search(track_name).results[0]
            if download_track.length <= 320:
                bot.edit_message_text('Downloading 🔰', msg.chat.id, message.id)
                download_track.streams.get_audio_only().download(filename=f'{justify_track_fname(track_name)}.mp3')

                bot.edit_message_text('Sending ⚙️', msg.chat.id, message.id)
                track_bytes = open(f'{justify_track_fname(track_name)}.mp3', 'rb').read()

                audio = bot.send_audio(msg.chat.id, audio=track_bytes, title=track_name, thumb=track.album_imgs.medium.bytes)
                bot.edit_message_text('Done ✅', msg.chat.id, message.id)

                remove(f'{justify_track_fname(track_name)}.mp3')
                add_file_id_to_json(track_full_name=track_name, file_id=f'{audio.audio.file_id}', thumb_url=track.album_imgs.medium.url)
            else:
                bot.edit_message_text('The length of the song you requested is > 5 minutes! 😖', msg.chat.id, message.id)
        elif triggered:
            bot.send_message(msg.chat.id, text="Your search query doesn't found! 😞\n"
                                               "Send me a spotify track link 🎧 || a youtube video link! 💾 (length ≤ 5 minutes)")
    except BaseException as err:
        info = f'{datetime.now().strftime("%Y/%m/%d_%H:%M_%f")} => {msg.chat.id}'

        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            telebot.types.InlineKeyboardButton('Bug Report 🐞🔧', url='https://t.me/ZXBTLKXC')
        )
        bot.send_message(msg.chat.id, reply_markup=markup, parse_mode='html',
                         text=f'An error has occurred! 🪫\n'
                              f'Video download stopped! ❌\n'
                              f'<b>[ERROR CODE: {info}]</b>')

        bot.send_message(env.SPOTIFY_LOG_CHANNEL_ID, parse_mode='html',
                         text=f'<b>BUG REPORT [{info}]</b>\n\n{err}')

        print(f'\n\n<b>BUG REPORT [{info}]</b>\n\n{err}')
        raise err


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(callback: telebot.types.CallbackQuery):
    match callback.data:
        case 'donate':
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                telebot.types.InlineKeyboardButton('Back ↩️', callback_data='main_menu'),
            )

            bot.edit_message_text('Come back here later! 🎃', callback.from_user.id, callback.message.id, reply_markup=markup)
        case 'main_menu':
            bot.edit_message_text("Hi! 👋\n"
                                  "I'm a bot 🤖 downloads music from spotify 🎧 and youtube 🎬 that's under 5️⃣ minutes long!\n"
                                  "Just send me link to the track and I'll download it for you! ✨", callback.from_user.id, callback.message.id, reply_markup=start_markup)


print(f'@{bot.get_me().username} | {bot.get_me().full_name} [{bot.get_me().id}]')

bot.skip_pending = True
bot.polling(none_stop=True)
