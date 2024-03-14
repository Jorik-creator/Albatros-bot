from aiogram import executor, Bot, Dispatcher

from config import Config
from handlers import register_handlers

config = Config()
bot = Bot(token=config.BOT_TOKEN)

if __name__ == "__main__":
    dp = Dispatcher(bot)
    register_handlers(dp)

    executor.start_polling(dp, skip_updates=True)
