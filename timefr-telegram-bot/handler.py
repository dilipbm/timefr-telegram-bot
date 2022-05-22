from collections import OrderedDict
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
from bson import ObjectId

from service import schedules as schedules_serv, find_user_favorites, build_user_fav_keyboard
from config import engine
from model import Favorite
from enums import TransportType, Direction


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


async def schedules(update: Update, context: CallbackContext.DEFAULT_TYPE):
    favorite: Favorite = await engine.find_one(Favorite)
    t_type = TransportType.from_str(favorite.transport_type)

    res = schedules_serv(
        type_=t_type,
        code=favorite.code,
        station=favorite.station,
        direction=Direction.A_AND_R.value,
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=res, parse_mode=ParseMode.HTML)


async def add_favorite(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print("start add favorite")
    # favorite = Favorite(**favorite_data)
    print(update.message.text)

    try:
        _, t_type, code = update.message.text.split(" ")
    except Exception as e:
        await update.message.reply_text("Something went wrong, use like this /add_fav bus 270")
        print(e)
        t_type = None
        code = None

    if t_type and code:
        t_type = TransportType.from_str(t_type)
        favorite = Favorite(
            code=code,
            user_id=update.message.from_user.id,
            transport_type=t_type.value,
            station="La+Cerisaie",
        )

        await engine.save(favorite)

        replay = "Done !"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=replay)


async def show_favorite(update: Update, context: CallbackContext.DEFAULT_TYPE):
    favorites = await find_user_favorites(update.message.from_user.id);
    keyboard = build_user_fav_keyboard(favorites=favorites)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    #await query.edit_message_text(text=f"Selected option: {query.data}")
    favorite: Favorite = await engine.find_one(Favorite, Favorite.id == ObjectId(query.data))
    t_type = TransportType.from_str(favorite.transport_type)

    res = schedules_serv(
        type_=t_type,
        code=favorite.code,
        station=favorite.station,
        direction=Direction.A_AND_R.value,
    )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=res, parse_mode=ParseMode.HTML)


async def help_command(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /start to test this bot.")

