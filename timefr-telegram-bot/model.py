from typing import Dict
from pydantic import BaseModel
from odmantic import Field, Model
from enums import TransportType, Action


class Favorite(Model):
    user_id: int
    transport_type: str
    code: str
    station: str


class CallbackData(BaseModel):
    action: Action
    data: Dict



