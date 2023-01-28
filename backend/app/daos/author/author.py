from abc import ABC, abstractmethod
from app.models.author.author import Author, AuthorCreate
from app.databases.sql import Session
from app.models.author.author import AuthorDB, AuthorMongo, AuthorRedis
from fastapi import Depends
from app.databases.sql import get_session
from pymongo.database import Database
from app.databases.mongo import db as mongodb
from redis import Redis
import redis
from redis.commands.json.path import Path
from app.databases.redis import get_redis, RedisDbs
import typing as t
class AuthorDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> Author:
        pass

    @abstractmethod
    def save(self, author: AuthorCreate) -> Author:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db: str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = AuthorDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = AuthorDAOMongo(mongodb)
        yield dao
    elif db == "redis":
        dao = AuthorDAORedis(get_redis(RedisDbs.AUTHORS))
        yield dao
    else:
        raise NotImplementedError()

class AuthorDAOSql(AuthorDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Author:
        author_sql = self.session.query(AuthorDB).filter(AuthorDB.id == id).first()
        if not author_sql:
            return None
        return Author.from_orm(author_sql)

    def save(self, author: AuthorCreate):
        author_sql = AuthorDB(**author.dict())
        if self.get_by_id(author.id):
            raise ValueError("exists")
        self.session.add(author_sql)
        self.session.commit()
        self.session.refresh(author_sql)
        return Author.from_orm(author_sql)
    def delete(self, id: str):
        author_sql = self.session.query(AuthorDB).filter(AuthorDB.id == id).first()
        self.session.delete(author_sql)


class AuthorDAOMongo(AuthorDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("authors")

    def get_by_id(self, id: str) -> t.Optional[Author]:
        author_bson = self.collection.find_one({'id': id})
        if author_bson:

            author_mongo = AuthorMongo(**author_bson)

            return Author.from_orm(author_mongo)
        else:
            return None

    def save(self, author: AuthorCreate) -> Author:
        author_mongo = AuthorMongo(**author.dict())
        author_json = author_mongo.dict(by_alias=True)
        if self.get_by_id(author.id):
            raise ValueError("exists")
        self.collection.insert_one(author_json).inserted_id
        ret = self.get_by_id(author.id)
        if ret is None:
            print(ret)
            raise ValueError("couldnt get after add") 
        else:
            return ret

    def delete(self, id: str):
        raise NotImplementedError()

class AuthorDAORedis(AuthorDAO):

    def __init__(self, client: Redis) -> None:
        super().__init__()
        self.client = client
        self.key_prefix = "author:"

    def get_by_id(self, id: str) -> t.Optional[Author]:
        model_json = self.client.json().get(self.key_prefix + id)
        if not model_json:
            return None
        author = Author(**model_json)
        return author
    def save(self, author: AuthorCreate) -> Author:
        author_redis = AuthorRedis(**author.dict())
        if self.client.json().get(self.key_prefix + author.id):
            raise ValueError("exists")
        self.client.json().set(self.key_prefix + author_redis.id, Path.root_path(), author_redis.dict())
        created = Author(**author.dict())
        return created

    def delete(self, id: str):
        raise NotImplementedError()