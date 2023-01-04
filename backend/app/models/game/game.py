from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, BigInteger
from pydantic import BaseModel
from sqlalchemy.orm import relationship
import typing as t
from app.databases.mongo import PyObjectId
from pydantic import Field
from bson import ObjectId

class GameDB(Base):
   __tablename__ = "games"
   id = Column(String(25), primary_key=True, index=True)
   name = Column(String(40))
   reviews = relationship("models.review.review.ReviewDB", back_populates="game", lazy="dynamic")
   
class GameMongo(BaseModel):
   mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
   id: str
   name: str

   class Config:
      allow_population_by_field_name = True
      arbitrary_types_allowed = True
      json_encoders = {ObjectId: str}
    
class GameBase(BaseModel):
   name: str
   id: str

class Game(GameBase):

   class Config:
      orm_mode = True

class GameCreate(GameBase):
   pass

# https://stackoverflow.com/questions/9088957/sqlalchemy-cannot-find-a-class-name
