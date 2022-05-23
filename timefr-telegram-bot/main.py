from cgi import test
import logging
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler, CallbackQueryHandler
from config import Setting

from handler import start, schedules, add_favorite, show_favorite, button

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    setting = Setting()
    application = ApplicationBuilder().token(setting.token).build()

    application.add_handler(CommandHandler(["start","help"], start))
    application.add_handler(CommandHandler("horaire", schedules))
    application.add_handler(CommandHandler("add_fav", add_favorite))
    application.add_handler(CommandHandler("show_fav", show_favorite))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

