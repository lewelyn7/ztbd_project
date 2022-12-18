from abc import ABC, abstractmethod
from app.models.author.author import Author, AuthorCreate
from app.databases.sql import Session
from app.models.author.author import AuthorDB
from fastapi import Depends
from app.databases.sql import get_session

class AuthorDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str):
        pass

    @abstractmethod
    def save(self, author: AuthorCreate) -> Author:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(session: Session = Depends(get_session)):
    dao = AuthorDAOSql(session)
    yield dao
    

class AuthorDAOSql(AuthorDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str):
        author_sql = self.session.query(AuthorDB).filter(AuthorDB.User.id == id).first()
        return Author.from_orm(author_sql)

    def save(self, author: AuthorCreate):
        author_sql = AuthorDB(**author.dict())
        self.session.add(author_sql)
        self.session.commit()
        self.session.refresh(author_sql)
        return Author.from_orm(author_sql)
    def delete(self, id: str):
        author_sql = self.session.query(AuthorDB).filter(AuthorDB.User.id == id).first()
        self.session.delete(author_sql)