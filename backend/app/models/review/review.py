from app.databases.sql import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime
from pydantic import Field
from bson import ObjectId
from app.databases.mongo import PyObjectId

from app.models.game.game import Game
from app.models.author.author import Author
class ReviewDB(Base):
    __tablename__ = "reviews"
    id = Column(String(25), primary_key=True, index=True)
    language = Column(String(25))
    content = Column(String(1000))
    timestamp_created = Column(DateTime)
    timestampe_updated = Column(DateTime)
    recommended = Column(Boolean)
    votes_helpful = Column(Integer)
    votes_funny = Column(Integer)
    weighted_vote_score = Column(Float)
    comment_count = Column(Float)
    steam_purchase = Column(Boolean)
    received_for_free = Column(Boolean)
    written_during_early_access = Column(Boolean)
    playtime_at_review = Column(BigInteger)

    author_id = Column(String(25), ForeignKey("authors.id"))
    # author = relationship("app.models.author.author.AuthorDB", back_populates="reviews")

    game_id = Column(String(25), ForeignKey("games.id"))
    # game = relationship("app.models.game.game.GameDB", back_populates="reviews")

class ReviewMongo(BaseModel):
    mongo_id: ObjectId = Field(default_factory=PyObjectId, alias="_id")
    id: str
    language: str
    content: str
    timestamp_created: datetime
    timestampe_updated: datetime
    recommended: bool
    votes_helpful: int
    votes_funny: int
    weighted_vote_score: float
    comment_count: int
    steam_purchase: bool
    received_for_free: bool
    written_during_early_access: bool
    playtime_at_review: int

    author_id: ObjectId
    game_id: ObjectId

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}



class ReviewBase(BaseModel):
    language: str
    content: str
    timestamp_created: datetime
    timestampe_updated: datetime
    recommended: bool
    votes_helpful: int
    votes_funny: int
    weighted_vote_score: float
    comment_count: int
    steam_purchase: bool
    received_for_free: bool
    written_during_early_access: bool
    playtime_at_review: int

    author_id: str
    game_id: str
    # author: Author
    # game: Game

    id: str

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):

    class Config:
        orm_mode = True