from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Row(BaseModel):
    user_id = TextField()
    img_encoding = BlobField()
    img_base64 = TextField()
    #created_date = DateTimeField(default=datetime.datetime.now)


def addUser(user_id, img_encoding, img_base64):
    t = Row.create(user_id=user_id, img_encoding=img_encoding, img_base64= img_base64)
    t.save()


def getUser_id(img_encoding):
    return Row.select().where(Row.img_encoding == img_encoding)


def checkout_db():
    for row in Row.select():
        print(Row.user_id, Row.img_base64)


def create_tables():
    with db:
        db.create_tables([Row])
        