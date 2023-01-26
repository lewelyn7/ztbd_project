from fastapi import APIRouter, HTTPException
from fastapi import status
from app.models.review.review import Review, ReviewCreate, ReviewDB
from app.models.author.author import AuthorDB
from app.daos.review.review import ReviewDAO, get_dao

from fastapi import Depends

from app.core.utils import raise_409

router = APIRouter(prefix="/api/reviews")

@router.post("/", response_model=Review)
def create_review(review: ReviewCreate, dao: ReviewDAO = Depends(get_dao)):
    created_review = raise_409(dao.save)(review)
    if not created_review:
        raise HTTPException(status_code=400, detail="already registered")
    return created_review

@router.get("/{id}", response_model=Review)
def get_review_by_id(id: str, dao: ReviewDAO = Depends(get_dao)):
    review = dao.get_by_id(id)
    if review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return review

def get_authors():
    pass