from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler
from bson import ObjectId

from service import (
    schedules as schedules_serv,
    find_user_favorites,
    build_user_fav_keyboard,
)
from config import engine
from model import Favorite, CallbackData
from enums import TransportType, Direction, Action


async def start(update: Update, context: CallbackContext.DEFAULT_TYPE):
    text = """
    Ceci est un bot qui permet d'obtenir les horaires de bus, métro, RER ou trambay\n
    <b>Utilisation</b>\n
    /help: Pour obtenir de l'aide\n
    /horaire: Obternir les horaires. Exemple d'utilisation /horaire bus 270 La cerisaie\n
    /add_fav: Ajouter a vos favoris. Exemple d'utilisation /add_fav bus 270 La cerisaie\n
    /show_fav: Afficher vos favoris.\n
    """
    await update.message.reply_text(text, parse_mode=ParseMode.HTML)


async def schedules(update: Update, context: CallbackContext.DEFAULT_TYPE):
    if len(context.args) < 4:
        await update.message.reply_text(
            "Mauvaise utilisation de la requête. Consulter l'aide /help"
        )
        return None

    transport_type_str = context.args[0]
    code = context.args[1]
    station = " ".join(context.args[2:])

    try:
        transport_type = TransportType.from_str(label=transport_type_str)
    except NotImplementedError:
        await update.message.reply_text(
            "Vous ne pouvez utiliser qu'une des valeurs suivante en deuxième argument : bus, métro, rer ou tramway."
        )
        return None

    res = schedules_serv(
        type_=transport_type,
        code=code,
        station=station,
        direction=Direction.A_AND_R.value,
    )

    callback_data = CallbackData(
        action=Action.ADD_TO_FAV,
        data={"code": code, "station": station, "type": transport_type},
    )

    keyboard = [
        [InlineKeyboardButton("Ajouter dans favoris", callback_data="callback_data")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        res, parse_mode=ParseMode.HTML, reply_markup=reply_markup
    )


async def add_favorite(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print("start add favorite")
    # favorite = Favorite(**favorite_data)
    print(update.message.text)

    try:
        _, t_type, code = update.message.text.split(" ")
    except Exception as e:
        await update.message.reply_text(
            "Something went wrong, use like this /add_fav bus 270"
        )
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
    favorites = await find_user_favorites(update.message.from_user.id)
    keyboard = build_user_fav_keyboard(favorites=favorites)

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)


async def button(update: Update, context: CallbackContext.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query

    await query.answer()

    # await query.edit_message_text(text=f"Selected option: {query.data}")
    favorite: Favorite = await engine.find_one(
        Favorite, Favorite.id == ObjectId(query.data)
    )
    t_type = TransportType.from_str(favorite.transport_type)

    res = schedules_serv(
        type_=t_type,
        code=favorite.code,
        station=favorite.station,
        direction=Direction.A_AND_R.value,
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=res, parse_mode=ParseMode.HTML
    )
