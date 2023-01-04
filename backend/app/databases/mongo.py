from bson import ObjectId
from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_URI)


db = client.get_database("perf_tester")

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