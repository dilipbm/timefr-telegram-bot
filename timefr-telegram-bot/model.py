from pydantic import BaseModel
from odmantic import Field, Model
from enums import TransportType


class Favorite(Model):
    user_id: str
    transport_type: str
    code: str
    station: str
