from peewee import (
    MySQLDatabase,
    CharField,
    Model,
)
from app.settings import DB_SETTINGS


db = MySQLDatabase(**DB_SETTINGS)


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db


class Player(BaseModel):
    name = CharField()


def create_tables():
    with db:
        db.create_tables([Player])
