from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.orm import relationship
from pydantic import BaseModel

 
class AuthorDB(Base):
    __tablename__ = "authors"
    id = Column(String(25), primary_key=True, index=True)
    num_of_games_owned = Column(Integer)
    num_reviews = Column(Integer)
    playtime_forever = Column(BigInteger)
    playtime_last_two_weeks = Column(BigInteger)

    reviews = relationship("app.models.review.review.ReviewDB", back_populates="author", lazy="dynamic")

class AuthorBase(BaseModel):
    num_of_games_owned: int
    num_reviews: int
    playtime_forever: int
    playtime_last_two_weeks: int

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: str

    class Config:
        orm_mode = True
