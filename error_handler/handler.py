import io
from datetime import datetime
import traceback
import aiogram
import settings


async def error_handler(update: aiogram.types.Update, exception: BaseException):
    bot = update.bot
    upd_message = update.message

    # idk what exception for this:
    # await upd_message.reply("Your search query doesn't found! 😞\n"
    #                         "Send me a spotify track link 🎧 || a youtube video link! 💾 (length ≤ 5 minutes)")

    markup = aiogram.types.InlineKeyboardMarkup(row_width=1)
    markup.add(aiogram.types.InlineKeyboardButton('Support 🔧', url='https://t.me/Zwylair'))

    info = f'\tTime: {datetime.now().strftime("%d.%m.%Y %H:%M")}\n' \
           f'\tUser: {upd_message.chat.id}'

    await upd_message.reply(
        text=f'An error was occurred, track downloading was stopped. Send the screenshot of this message to support.\n\n'
             f'Technical info:\n'
             f'{info}',
        reply_markup=markup
    )

    formatted_exception = traceback.format_exception(type(exception), exception, exception.__traceback__)
    formatted_exception_str = ''.join(formatted_exception)

    i_f = aiogram.types.InputFile(io.BytesIO(formatted_exception_str.encode()))
    i_f.filename = 'traceback.log'

    await bot.send_document(
        settings.LOG_CHANNEL_ID,
        caption=f'Error:\n\n{info}',
        document=i_f
    )
