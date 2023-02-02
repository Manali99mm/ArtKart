import os
from dotenv import load_dotenv
import datetime
from pymongo import MongoClient

load_dotenv()

class ConfigClass(object):
    MONGODB_SETTINGS = {
        'db': os.environ.get('MONGO_DBNAME'),
        'host': os.environ.get('MONGO_URI'),
    }
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET')
    JWT_ACCESS_TOKEN_EXPIRES= datetime.timedelta(days=1)

    def create_collection(coll_name, schema):
        client = MongoClient(os.environ.get('MONGO_URI'))
        db = client[os.environ.get('MONGO_DBNAME')]
        db.create_collection(coll_name, validator={
            '$jsonSchema': schema
        })