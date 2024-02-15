import os
from dotenv import load_dotenv
from peewee import MySQLDatabase

load_dotenv()

db = MySQLDatabase(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD', default=''),
    database=os.getenv('DB_NAME'),
    charset=os.getenv('DB_CHARSET'))
