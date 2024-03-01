from peewee import *

from DataBase.config import db


class Consultant(Model):
    id = AutoField()
    name = CharField()
    phone = CharField()
    chat_id = IntegerField(null=True)
    all_message = TextField()
    birthday_message = TextField()

    class Meta:
        db_table = 'consultants'
        database = db

Consultant.create_table()
