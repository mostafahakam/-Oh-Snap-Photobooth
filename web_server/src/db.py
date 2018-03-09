from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db

class Auth(BaseModel):
	user_id = TextField(unique=True)
	password = TextField()

class Row(BaseModel):
    user_id = TextField()
    img_encoding = BlobField()
    file_name = TextField()
    #created_date = DateTimeField(default=datetime.datetime.now)


def addUser(user_id, img_encoding, file_name):
    t = Row.create(user_id=user_id, img_encoding=img_encoding, file_name= file_name)
    t.save()


def getUser_id(img_encoding):
    return Row.select().where(Row.img_encoding == img_encoding)


def checkout_db():
    for row in Row.select():
        print(Row.user_id, Row.img_base64)

def new_User(user_id, password):
	t = Auth.create(user_id=user_id, password=password)
	t.save()

def get_User_pass(user_id):
	for row in Auth.select().where(Auth.user_id == user_id):
		return row.password

def create_tables():
    with db:
        db.create_tables([Row, Auth])
        