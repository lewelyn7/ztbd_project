from abc import ABC, abstractmethod
from app.models.author.author import Author, AuthorCreate
from app.databases.sql import Session
from app.models.author.author import AuthorDB, AuthorMongo
from fastapi import Depends
from app.databases.sql import get_session
from pymongo.database import Database
from app.databases.mongo import db as mongodb
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
    else:
        raise NotImplementedError()

class AuthorDAOSql(AuthorDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str) -> Author:
        author_sql = self.session.query(AuthorDB).filter(AuthorDB.id == id).first()
        return Author.from_orm(author_sql)

    def save(self, author: AuthorCreate):
        author_sql = AuthorDB(**author.dict())
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