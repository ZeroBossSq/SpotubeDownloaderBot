import asyncio
import logging
import os
import sqlite3

import aiogram
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import message_handler
import error_handler
import settings
import zwyFramework

server = zwyFramework.pinger.PingServer('0.0.0.0', 80)
client = zwyFramework.pinger.PingClient('http://127.0.0.1', 80)

logger = logging.getLogger(__name__)
logging.basicConfig(format='[%(asctime)s | %(levelname)s | %(name)s]: %(message)s')
logger.setLevel(logging.INFO)

bot = aiogram.Bot(settings.TOKEN)
dp = aiogram.Dispatcher(bot)
spotify_credentials = SpotifyClientCredentials(client_id=settings.SPOTIFY_CLIENT_ID,
                                               client_secret=settings.SPOTIFY_TOKEN)
spotify_client = Spotify(client_credentials_manager=spotify_credentials)


@dp.message_handler(commands=['start', 'help'])
async def start(message: aiogram.types.Message):
    markup = aiogram.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        # aiogram.types.InlineKeyboardButton('Donate 💎', callback_data='donate'),
        aiogram.types.InlineKeyboardButton('Support 🧰', url='https://t.me/zwylair')
    )

    text = "Hi! 👋\n" \
           "I'm a bot 🤖 downloads music from spotify 🎧 and youtube 🎬 that's under 5️⃣ minutes long!\n" \
           "Just send me link to the track and I'll download it for you! ✨"

    await message.reply(text, reply_markup=markup)


async def main():
    server.run()
    client.run()

    wipe_db = False
    sql = sqlite3.connect(settings.DB_FN)
    got_dumps = [i.to_string() for i in zwyFramework.get_sqlite_dumps(sql.cursor())]

    if not got_dumps:
        wipe_db = True

    for got, original in zip(got_dumps, settings.DB_DUMPS):
        if got != original:
            wipe_db = True
            break

    if wipe_db:
        sql.close()
        os.remove(settings.DB_FN)

        with sqlite3.connect(settings.DB_FN) as sql:
            for i in settings.DB_DUMPS:
                sql.execute(i)
            sql.commit()

    me = await bot.get_me()

    error_handler.setup(dp)
    message_handler.setup(dp, spotify_client)

    logger.info(f'Sir! @{me.username} [{me.id}] here!')
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
