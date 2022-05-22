from pydantic import BaseSettings
from odmantic import AIOEngine
from motor.motor_asyncio import AsyncIOMotorClient


class Setting(BaseSettings):
    token: str
    mongodb_url: str
    mongodb_database: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


setting = Setting()
client = AsyncIOMotorClient(setting.mongodb_url)
engine = AIOEngine(motor_client=client, database=setting.mongodb_database)

