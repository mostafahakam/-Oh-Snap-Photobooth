from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase
import datetime

db = SqliteExtDatabase('database.db')


class BaseModel(Model):
    class Meta:
        database = db


class Auth(BaseModel):
    user_id = TextField()
    password = TextField()


class Row(BaseModel):
    user_id = TextField()
    img_encoding = BlobField()
    file_name = TextField()
    # created_date = DateTimeField(default=datetime.datetime.now)


class Social(BaseModel):
    user_id = TextField()
    instagram_handle = TextField()
    twitter_handle = TextField()
    facebook_handle = TextField()


def addUser(user_id, img_encoding, file_name):
    t = Row.create(user_id=user_id, img_encoding=img_encoding, file_name=file_name)
    t.save()


def addUser_social(user_id, ig_handle, tw_handle, fb_handle):
    query = Social.delete().where(Social.user_id == user_id)
    query.execute()
    s = Social.create(user_id=user_id, instagram_handle=ig_handle, twitter_handle=tw_handle, facebook_handle=fb_handle)
    s.save()


def getUser_id(img_encoding):
    return Row.select().where(Row.img_encoding == img_encoding)


def checkout_db():
    for row in Auth.select():
        print(row.user_id, row.password)


def new_User(user_id, password):
    if len(Auth.select().where(Auth.user_id == user_id)) > 0:
        return 0
    else:
        t = Auth.create(user_id=user_id, password=password)
        t.save()
        return 1


def get_User_pass(user_id):
    hashed_pass = "None"

    for row in Auth.select().where(Auth.user_id == user_id):
        hashed_pass = row.password

    if hashed_pass != "None":
        return hashed_pass
    else:
        return "Fail"


def clear_auth_table():
    query = Auth.delete()
    query.execute()


def clear_row_table():
    query = Row.delete()
    query.execute()


def clear_social_table():
    query = Social.delete()
    query.execute()


def clear_all_tables():
    clear_auth_table()
    clear_row_table()
    clear_social_table()


def create_tables():
    with db:
        db.create_tables([Row, Auth, Social])
