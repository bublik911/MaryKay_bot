from peewee import *
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(
    host='127.0.0.1',
    user='user',
    password='Root767!',
    database='mk',
    timeout=0,
    charset='utf8mb4'
)
# db.connect()


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


Consultant.create_table()
Client.create_table()
# db.close()
