from string import ascii_letters
from os import remove, getenv

import pytube
import telebot

from Track.track import SpotiClient

bot = telebot.TeleBot(getenv('spotify_downloader_bot_token'))

s_client = SpotiClient(client_id=getenv('spotify_downloader_bot_client_id'),
                       client_secret=getenv('spotify_downloader_bot_client_secret'))


def justify_track_fname(track_full_name: str):
    return ''.join([i for i in list(track_full_name) if i in ascii_letters])


@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        telebot.types.InlineKeyboardButton('Donate', callback_data='donate'),
        telebot.types.InlineKeyboardButton('Support', url='https://t.me/ZXBTLKXC')
    )

    bot.send_message(msg.chat.id, "Hi! 👋\n"
                                  "I'm a bot 🤖 downloads music from spotify 🎧 and youtube 🎬 that's under 5️⃣ minutes long!\n"
                                  "Just send me link to the track and I'll download it for you! ✨", reply_markup=markup)


@bot.message_handler()
def msg_handler(msg: telebot.types.Message):
    try:
        track_name = ''
        founded = False

        if 'spotify' in msg.text:
            bot.send_message(msg.chat.id, '⏳')

            track = s_client.get_track(msg.text)

            bot.send_photo(msg.chat.id, photo=track.album_imgs.medium.bytes,
                           caption=f'`{track.full_name}` ({track.duration} min) (Images: '
                                   f'[Large]({track.album_imgs.large.url}), [Medium]({track.album_imgs.medium.url}), [Small]({track.album_imgs.small.url}))',
                           parse_mode='MARKDOWN')

            track_name = track.full_name
            founded = True
        elif 'youtu' in msg.text:
            bot.send_message(msg.chat.id, '⏳')

            track = pytube.YouTube(msg.text)
            track_name = f'{track.title} - {track.author}'

            bot.send_photo(msg.chat.id, track.thumbnail_url, track_name)
            founded = True

        if founded:
            # Trying to find song in the logs
            message = bot.send_message(msg.chat.id, text='Searching 🔍')
            download_track: pytube.YouTube = pytube.Search(track_name).results[0]

            if download_track.length <= 320:
                bot.edit_message_text('Downloading 🔰', msg.chat.id, message.id)
                download_track.streams.get_audio_only().download(filename=f'{justify_track_fname(track_name)}.mp3')

                bot.edit_message_text('Sending ⚙️', msg.chat.id, message.id)
                track_bytes = open(f'{justify_track_fname(track_name)}.mp3', 'rb').read()

                bot.send_audio(msg.chat.id, audio=track_bytes, title=track_name)
                bot.edit_message_text('Done ✅', msg.chat.id, message.id)

                remove(f'{justify_track_fname(track_name)}.mp3')
            else:
                bot.edit_message_text('The length of the song you requested is > 5 minutes! 😖', msg.chat.id, message.id)
        else:
            bot.send_message(msg.chat.id, text="Your search query doesn't found! 😞\n"
                                               "Send me a spotify track link 🎧 || a youtube video link! 💾 (length ≤ 5 minutes)")
    except BaseException:
        bot.send_message(msg.chat.id, text='An error has occurred! 🪫\n'
                                           'Video download stopped! ❌')


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
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                telebot.types.InlineKeyboardButton('Donate 💎', callback_data='donate'),
                telebot.types.InlineKeyboardButton('Support 🧰', url='https://t.me/ZXBTLKXC')
            )

            bot.edit_message_text("Hi! 👋\n"
                                  "I'm a bot 🤖 downloads music from spotify 🎧 and youtube 🎬 that's under 5️⃣ minutes long!\n"
                                  "Just send me link to the track and I'll download it for you! ✨",
                                  callback.from_user.id, callback.message.id, reply_markup=markup)


print(f'@{bot.get_me().username} | {bot.get_me().full_name} [{bot.get_me().id}]')

bot.skip_pending = True
bot.polling(none_stop=True)
