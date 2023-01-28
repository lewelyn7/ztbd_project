from abc import ABC, abstractmethod
from app.models.review.review import Review, ReviewCreate, ReviewMongo, ReviewRedis
from app.databases.sql import Session
from app.models.review.review import ReviewDB
from fastapi import Depends
from app.databases.sql import get_session
from typing import Optional
from redis import Redis
from redis.commands.search.query import Query
import json

from redis.commands.json.path import Path
from app.databases.redis import get_redis, RedisDbs
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

    @abstractmethod
    def search(self, query: t.Dict[str,str], limit: int = 10) -> t.List[Review]:
        pass

def get_dao(db:str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = ReviewDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = ReviewDAOMongo(mongodb)
        yield dao
    elif db == "redis":
        dao = ReviewDAORedis(get_redis(RedisDbs.REVIEWS))
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
        if self.get_by_id(review.id):
            raise ValueError("exists")
        self.session.add(review_sql)
        self.session.commit()
        self.session.refresh(review_sql)
        return Review.from_orm(review_sql)
    def delete(self, id: str):
        review_sql = self.session.query(ReviewDB).filter(ReviewDB.id == id).first()
        self.session.delete(review_sql)
    
    def search(self, query: t.Dict[str, str], limit: int = 10) -> t.List[Review]:
        q = self.session.query(ReviewDB)
        for attr, value in query.items():
            q = q.filter(getattr(ReviewDB, attr) == value)
        q_results = q.limit(limit).all()
        results = [Review.from_orm(r) for r in q_results]

        return results

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

    def search(self, query: t.Dict[str, str], limit: int = 10) -> t.List[Review]:
        find_result = self.collection.find(query, limit=limit)
        result = [r for r in find_result]
        print(result)
        result = [Review.from_orm(r) for r in find_result]
        return result

class ReviewDAORedis(ReviewDAO):

    def __init__(self, client: Redis) -> None:
        super().__init__()
        self.client = client
        self.key_prefix = "review:"

    def get_by_id(self, id: str) -> t.Optional[Review]:
        model_json = self.client.json().get(self.key_prefix + id)
        if not model_json:
            return None
        model = Review(**model_json)
        return model 
        
    def save(self, review: ReviewCreate) -> Review:
        model_redis = ReviewRedis(**review.dict())
        if self.client.json().get(self.key_prefix + review.id):
            raise ValueError("exists")
        model_json = json.loads(model_redis.json())
        self.client.json().set(self.key_prefix + model_redis.id, Path.root_path(), model_json)
        created = Review(**review.dict())
        return created

    def delete(self, id: str):
        raise NotImplementedError()

    # def search(self, query: t.Dict[str, str], limit: int = 10) -> t.List[Review]:
    #     built_query_str = "FT.SEARCH reviews_idx "
    #     for k, v in query.items():
    #         built_query_str += f"@{k}:{v}"
    #         built_query_str += " "

    #     built_query_str += f"LIMIT 0 {limit}"
    #     print(built_query_str)
    #     ret = self.client.execute_command(built_query_str)
    #     print(ret)
    #     return []

    def search(self, query: t.Dict[str, str], limit: int = 10) -> t.List[Review]:

        key, value = [e for e in query.items()][0]
        ret = self.client.ft('reviews_idx').search(Query(value).limit_fields(key))
        print(ret)
        return []