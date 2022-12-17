from app.database import Base
from sqlalchemy import Column, String, Integer, BigInteger
from pydantic import BaseModel
from sqlalchemy.orm import relationship
from ..review.review import Review
import typing as t

class GameDB:
   __tablename__ = "games"
   id = Column(String(25), primary_key=True, index=True)
   name = Column(String(40))
   reviews = relationship("ReviewDB", back_populates="games", lazy="dynamic")
   
    
class GameBase(BaseModel):
   name: str
   reviews: t.List[Review]

class Game(GameBase):
   id: str

   class Config:
      orm_mode = True

class GameCreate(GameBase):
   pass