import logging
from telegram import Update
from pymongo import MongoClient
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
from config import Setting

from handler import start, schedules, add_favorite

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    setting = Setting()
    application = ApplicationBuilder().token(setting.token).build()

    start_handler = CommandHandler("start", start)
    application.add_handler(start_handler)

    schesules_handler = CommandHandler("horaire", schedules)
    application.add_handler(schesules_handler)

    add_favorite_handler = CommandHandler("add_favorite", add_favorite)
    application.add_handler(add_favorite_handler)

    application.run_polling()

