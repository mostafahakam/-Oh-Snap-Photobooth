from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Row(BaseModel):
    user_id = TextField()
    img_encoding = TextField()
    img_base64 = TextField()
    #created_date = DateTimeField(default=datetime.datetime.now)


def addUser(user_id, img_encoding, img_base64):
    t = Row.create(user_id=user_id, img_encoding=img_encoding, img_base64= img_base64)
    t.save()


def getUser_id(img_encoding):
    return Row.select().where(Row.img_encoding == img_encoding)


def checkout_db():
	for row in Row.select():
		print(row.user_id, row.img_base64)