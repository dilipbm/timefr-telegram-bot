import httpx
import logging
from config import engine
from enums import Direction, TransportType


def schedules(type_: TransportType, code: str, station: str, direction: Direction):
    if type_ == TransportType.BUS:
        type_str = "buses"
    else:
        return False

    url = f"https://api-ratp.pierre-grimaud.fr/v4/schedules/{type_str}/{code}/{station}/{Direction.A_AND_R.value}"
    response = httpx.get(url)
    if response.status_code == 200:
        return response.json()
