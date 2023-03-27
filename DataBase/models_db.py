from peewee import *

db = MySQLDatabase(
    host='127.0.0.1',
    user='root',
    password='',
    database='mk'
)
db.connect()


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
db.close()
