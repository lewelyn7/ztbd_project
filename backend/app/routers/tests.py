import typing as t
from fastapi import APIRouter, HTTPException
from fastapi import status
from app.models.review.review import Review, ReviewCreate, ReviewDB
from app.models.author.author import AuthorDB
from app.daos.review import review
from app.daos.game import game
from app.daos.author import author
from app.models.test_results.test_results import SingleDbResult

from fastapi import Depends

from app.core.utils import raise_409
from dataclasses import dataclass
import time

router = APIRouter(prefix="/api/tests")

@dataclass
class CommonSettings:
    reviews_dao: review.ReviewDAO
    games_dao: game.GameDAO
    authors_dao: author.AuthorDAO

def get_common_settings(
    games_dao: game.GameDAO = Depends(game.get_dao),
    reviews_dao: review.ReviewDAO = Depends(review.get_dao),
    authors_dao: author.AuthorDAO = Depends(author.get_dao)
):
    return CommonSettings(
        reviews_dao=reviews_dao,
        games_dao=games_dao,
        authors_dao=authors_dao
    )



@router.get("/0", response_model=SingleDbResult)
def test_case0(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"author_id": "schinesea"})
        # print(len(result))
        end = time.time()        
        times.append(end - start)

    return SingleDbResult(times=times)
