from abc import ABC, abstractmethod
from app.models.review.review import Review, ReviewCreate, ReviewMongo
from app.databases.sql import Session
from app.models.review.review import ReviewDB
from fastapi import Depends
from app.databases.sql import get_session
from typing import Optional

from app.databases.mongo import db as mongodb
from pymongo.database import Database
import typing as t


class ReviewDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[Review]:
        pass

    @abstractmethod
    def save(self, review: ReviewCreate) -> Review:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db:str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = ReviewDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = ReviewDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()
    

class ReviewDAOSql(ReviewDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Optional[Review]:
        review_sql = self.session.query(ReviewDB).filter(ReviewDB.id == id).first()
        if not review_sql:
            return None
        return Review.from_orm(review_sql)

    def save(self, review: ReviewCreate):
        review_sql = ReviewDB(**review.dict())
        self.session.add(review_sql)
        self.session.commit()
        self.session.refresh(review_sql)
        return Review.from_orm(review_sql)
    def delete(self, id: str):
        review_sql = self.session.query(ReviewDB).filter(ReviewDB.id == id).first()
        self.session.delete(review_sql)

class ReviewDAOMongo(ReviewDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("reviews")

    def get_by_id(self, id: str) -> t.Optional[Review]:
        model_bson = self.collection.find_one({'id': id})
        if model_bson:
            model_mongo = ReviewMongo(**model_bson)

            return Review.from_orm(model_mongo)
        else:
            return None

    def save(self, model_create: ReviewCreate) -> Review:
        model_mongo = ReviewMongo(**model_create.dict())
        model_json = model_mongo.dict(by_alias=True)
        if self.get_by_id(model_mongo.id):
            raise ValueError("exists")
        self.collection.insert_one(model_json)
        ret = self.get_by_id(model_create.id)
        if not ret:
            raise ValueError("couldnt get after add") 
        else:
            return ret

    def delete(self, id: str):
        raise NotImplementedError()
