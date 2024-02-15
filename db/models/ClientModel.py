from peewee import *

from db.models.ConsultantModel import Consultant
from db.config import db


class Client(Model):
    pid = ForeignKeyField(Consultant)
    name = CharField()
    phone = CharField()
    chat_id = IntegerField(null=True)
    date = DateField()
    deleted_at = DateField(null=True)

    class Meta:
        db_table = 'client'
        database = db

Client.create_table()
