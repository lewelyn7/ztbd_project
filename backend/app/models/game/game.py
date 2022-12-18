from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, BigInteger
from pydantic import BaseModel
from sqlalchemy.orm import relationship
import typing as t

class GameDB(Base):
   __tablename__ = "games"
   id = Column(String(25), primary_key=True, index=True)
   name = Column(String(40))
   reviews = relationship("models.review.review.ReviewDB", back_populates="game", lazy="dynamic")
   
    
class GameBase(BaseModel):
   name: str

class Game(GameBase):
   id: str

   class Config:
      orm_mode = True

class GameCreate(GameBase):
   pass

# https://stackoverflow.com/questions/9088957/sqlalchemy-cannot-find-a-class-name
