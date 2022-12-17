from app.database import Base
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Float, BigInteger
from sqlalchemy.orm import relationship
from pydantic import BaseModel
from datetime import datetime

class ReviewDB(Base):
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

    author = relationship("AuthorDB", back_populates="reviews")
    game = relationship("GameDB", back_populates="reviews")




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

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: str

    class Config:
        orm_mode = True