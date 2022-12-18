from fastapi import APIRouter, HTTPException
from app.models.author.author import Author, AuthorCreate
from app.models.author.author import AuthorDB
from app.models.review.review import ReviewDB
from app.models.game.game import GameDB
from app.daos.author.author import AuthorDAO, get_dao

from fastapi import Depends
router = APIRouter(prefix="/authors")
@router.post("/", response_model=Author)
def create_user(author: AuthorCreate, dao: AuthorDAO = Depends(get_dao)):
    created_author = dao.save(author)
    if created_author:
        raise HTTPException(status_code=400, detail="already registered")
    return created_author