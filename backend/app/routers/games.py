
from fastapi import APIRouter, HTTPException
from app.models.game.game import Game, GameCreate
from app.models.author.author import AuthorDB
from app.models.review.review import ReviewDB
from app.models.game.game import GameDB
from app.daos.game.game import GameDAO, get_dao
from app.core.utils import raise_409

from fastapi import Depends

router = APIRouter(prefix="/games")

@router.post("/", response_model=Game)
def create_game(game: GameCreate, dao: GameDAO = Depends(get_dao)):
    created_game = raise_409(dao.save)(game)
    if not created_game:
        raise HTTPException(status_code=400, detail="already registered")
    return created_game

@router.get("/{id}", response_model=Game)
def get_author_by_id(id: str, dao: GameDAO = Depends(get_dao)):
    author = dao.get_by_id(id)
    return author

def get_authors():
    pass