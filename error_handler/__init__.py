import aiogram
import error_handler.handler


def setup(dp: aiogram.Dispatcher):
    dp.register_errors_handler(error_handler.handler.error_handler)
