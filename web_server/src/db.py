from peewee import *
from playhouse.postgres_ext import *
import datetime

db = PostgresqlExtDatabase('database', user='postgres')


class BaseExtModel(Model):
    class Meta:
        database = db


class Row(BaseExtModel):
    user_id = TextField()
    img_encoding = ArrayField(CharField)
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