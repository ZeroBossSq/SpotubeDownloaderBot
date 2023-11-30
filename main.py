import asyncio
import logging
import aiogram
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import message_handler
import error_handler
import settings
import backgrounds

backgrounds.start_keeping()

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
    me = await bot.get_me()

    error_handler.setup(dp)
    message_handler.setup(dp, spotify_client)

    logger.info(f'Sir! @{me.username} [{me.id}] here!')
    await dp.skip_updates()
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
