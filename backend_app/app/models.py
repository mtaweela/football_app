from peewee import (
    MySQLDatabase,
    Model,
    CharField,
    TextField,
    IntegerField,
    ForeignKeyField,
)
from app.settings import DB_SETTINGS


db = MySQLDatabase(**DB_SETTINGS)


class BaseModel(Model):
    """A base model that will use our MySQL database"""

    class Meta:
        database = db


class Nationality(BaseModel):
    name = CharField(null=False, unique=True)


class Club(BaseModel):
    name = CharField(null=False, unique=True)


class Player(BaseModel):
    name = CharField(null=True)
    age = IntegerField(null=True)
    nationality = ForeignKeyField(
        column_name="nationality_id", field="id", model=Nationality
    )
    club = ForeignKeyField(column_name="club_id", field="id", model=Club)
    photo = TextField(null=True)
    overall = IntegerField(null=True)
    value = IntegerField(null=True)


def create_tables():
    with db:
        db.create_tables([Player])
