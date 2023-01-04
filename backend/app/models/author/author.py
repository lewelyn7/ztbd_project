from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field, validator
from app.databases.mongo import PyObjectId
from bson import ObjectId

 
class AuthorDB(Base):
    __tablename__ = "authors"
    id = Column(String(25), primary_key=True, index=True)
    num_of_games_owned = Column(Integer)
    num_reviews = Column(Integer)
    playtime_forever = Column(BigInteger)
    playtime_last_two_weeks = Column(BigInteger)

    reviews = relationship("app.models.review.review.ReviewDB", back_populates="author", lazy="dynamic")

class AuthorMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: str
    num_of_games_owned: int
    num_reviews: int
    playtime_forever: int
    playtime_last_two_weeks: int

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AuthorBase(BaseModel):
    num_of_games_owned: int
    num_reviews: int
    playtime_forever: int
    playtime_last_two_weeks: int
    id: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):

    class Config:
        orm_mode = True
