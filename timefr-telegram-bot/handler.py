from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackContext, CommandHandler

from service import schedules as schedules_serv
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

    try:
        schedules = res.get("result").get("schedules")
    except KeyError:
        schedules = []

    if schedules:
        schedules_str = "Prochaines passages \n"
        for schedule in schedules:
            schedules_str += f"Destination: {schedule.get('destination')}\n"
            schedules_str += f"Passage dans: {schedule.get('message')}\n"
            schedules_str += "-----\n"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=schedules_str)


async def add_favorite(update: Update, context: CallbackContext.DEFAULT_TYPE):
    print("start add favorite")
    # favorite = Favorite(**favorite_data)
    print(update.message.text)

    try:
        _, t_type, code = update.message.text.split(" ")
    except Exception as e:
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
    else:
        replay = "Error !!!"

    await context.bot.send_message(chat_id=update.effective_chat.id, text=replay)
