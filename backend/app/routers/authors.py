from fastapi import APIRouter, HTTPException
from app.models.author.author import Author, AuthorCreate
from app.models.author.author import AuthorDB
from app.models.review.review import ReviewDB
from app.models.game.game import GameDB
from app.daos.author.author import AuthorDAO, get_dao
from fastapi import status
from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/api/authors")


@router.post("/", response_model=Author)
def create_author(author: AuthorCreate, db: str, dao: AuthorDAO = Depends(get_dao)):
    created_author = raise_409(dao.save)(author)
    return created_author

@router.get("/{id}", response_model=Author)
def get_author_by_id(id: str, db: str, dao: AuthorDAO = Depends(get_dao)):
    author = dao.get_by_id(id)
    if not author:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return author

def get_authors():
    pass