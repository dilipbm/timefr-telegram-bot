from collections import OrderedDict
from typing import List
import httpx
from telegram import InlineKeyboardButton
from config import engine
from model import Favorite
from enums import Direction, TransportType

async def find_user_favorites(user_id: str) -> List[Favorite]:
    result = await engine.find(Favorite)
    return result

def build_user_fav_keyboard(favorites: List[Favorite]):
    keyboard = []
    if favorites:
        for fav in favorites:
            inlinekeyboard = []
            inlinekeyboard.append(InlineKeyboardButton(f"{fav.code} - {fav.station.replace('+',' ')}", callback_data=str(fav.id)))
            keyboard.append(inlinekeyboard)

    return keyboard


def schedules(type_: TransportType, code: str, station: str, direction: Direction):
    response_str = "Horaire non disponible"

    if type_ == TransportType.BUS:
        type_str = "buses"
    else:
        return False

    url = f"https://api-ratp.pierre-grimaud.fr/v4/schedules/{type_str}/{code}/{station}/{Direction.A_AND_R.value}"
    response = httpx.get(url)
    if response.status_code == 200:
        schedules = response.json().get("result", {}).get("schedules", [])

        if schedules:
            grouped_by_destination = OrderedDict()
            for schedule in schedules:
                destination = schedule.get("destination", "NO DEST")
                time = schedule.get("message", "NO DISPO")

                if destination in grouped_by_destination.keys():
                    grouped_by_destination[destination].append(time)
                else:
                    grouped_by_destination[destination] = [time]

            response_str = f"Arrêt : <strong> {code} - {station.replace('+',' ')}</strong>\n\n"
            for destination, time in grouped_by_destination.items():
                response_str += f"{destination}\n"
                response_str += ", ".join(time)
                response_str += "\n"
                response_str += "-----\n"

    return response_str

