from abc import ABC, abstractmethod
from app.models.game.game import Game, GameCreate, GameMongo
from app.databases.sql import Session
from app.models.game.game import GameDB
from fastapi import Depends
from app.databases.sql import get_session
from app.databases.mongo import db as mongodb
from pymongo.database import Database
import typing as t

class GameDAO(ABC):

    @abstractmethod
    def get_by_id(self, id: str) -> t.Optional[Game]:
        pass

    @abstractmethod
    def save(self, game: GameCreate) -> Game:
        pass

    @abstractmethod
    def delete(self, id: str):
        pass

def get_dao(db: str, session: Session = Depends(get_session)):
    if db == "postgresql":
        dao = GameDAOSql(session)
        yield dao
    elif db == "mongodb":
        dao = GameDAOMongo(mongodb)
        yield dao
    else:
        raise NotImplementedError()
    

class GameDAOSql(GameDAO):

    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def get_by_id(self, id: str):
        game_sql = self.session.query(GameDB).filter(GameDB.id == id).first()
        if not game_sql:
            return None
        return Game.from_orm(game_sql)

    def save(self, game: GameCreate):
        game_sql = GameDB(**game.dict())
        if self.get_by_id(game.id):
            raise ValueError("exists")


        self.session.add(game_sql)
        self.session.commit()
        self.session.refresh(game_sql)
        return Game.from_orm(game_sql)
    def delete(self, id: str):
        game_sql = self.session.query(GameDB).filter(GameDB.id == id).first()
        self.session.delete(game_sql)

class GameDAOMongo(GameDAO):

    def __init__(self, db: Database) -> None:
        super().__init__()
        self.db = db
        self.collection = db.get_collection("games")

    def get_by_id(self, id: str) -> t.Optional[Game]:
        model_bson = self.collection.find_one({'id': id})
        if model_bson:
            model_mongo = GameMongo(**model_bson)

            return Game.from_orm(model_mongo)
        else:
            return None

    def save(self, model_create: GameCreate) -> Game:
        model_mongo = GameMongo(**model_create.dict())
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