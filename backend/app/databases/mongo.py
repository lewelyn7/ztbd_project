from bson import ObjectId
from pymongo import MongoClient, ASCENDING, HASHED
from app.core.config import settings

client = MongoClient(settings.MONGODB_URI)


db = client.get_database("perf_tester")
db['authors'].create_index([('id', ASCENDING)], unique=True)
db['games'].create_index([('id', ASCENDING)], unique=True)
db['reviews'].create_index([('id', ASCENDING)], unique=True)
db['reviews'].create_index([('author_id', ASCENDING)])
db['reviews'].create_index([('game_id', ASCENDING)])

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")