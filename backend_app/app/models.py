from peewee import (
    MySQLDatabase,
    Model,
    PrimaryKeyField,
    CharField,
    TextField,
    IntegerField,
    FloatField,
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
    id = PrimaryKeyField()
    name = CharField(null=True)
    age = IntegerField(null=True)
    nationality = ForeignKeyField(
        column_name="nationality_id", field="id", model=Nationality, null=True
    )
    club = ForeignKeyField(column_name="club_id", field="id", model=Club, null=True)
    photo = TextField(null=True)
    overall = IntegerField(null=True)
    value = IntegerField(null=True)
    position = CharField(null=True)


def create_schema():
    with db:
        db.create_tables([Nationality, Club, Player])


def add_data_from_csv():
    import csv

    with open("data.csv", newline="") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=",", quotechar="|")
        fields = next(csvreader)

        data_source = [
            {
                "name": row[2],
                "age": row[3],
                "nationality": Nationality.get_or_create(name=row[5])[0].id,
                "club": Club.get_or_create(name=row[9])[0].id,
                "photo": row[4],
                "overall": row[7],
                "value": row[11].replace("€", "").replace("M", "").replace("K", ""),
                "position": row[21],
            }
            for row in csvreader
        ]
        # print(data_source)
        Player.insert_many(data_source).execute()
