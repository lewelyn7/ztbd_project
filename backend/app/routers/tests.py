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
from app.databases.redis import get_redis, RedisDbs
from app.databases.mongo import db as mongodb
from app.databases.sql import get_session

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
        result = common_settings.reviews_dao.search({"author_id": "string"})
        # print(len(result))
        end = time.time()
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/1", response_model=SingleDbResult)
def test_case1(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"language": "schinesea"})
        # print(len(result))
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/2", response_model=SingleDbResult)
def test_case2(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"language": "not exist"})
        # print(len(result))
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/3", response_model=SingleDbResult)
def test_case3(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"language": "\"ukr\""})
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)
    
@router.get("/stats")
def get_stats():
    stats = {
        'redis': {
            'reviews' : {},
            'games' : {},
            'authors' : {},
        },
        'mongodb': {
            'reviews' : {},
            'games' : {},
            'authors' : {},
        },
        'postgresql': {
            'reviews' : {},
            'games' : {},
            'authors' : {},
        }

    }

    stats['redis']['reviews']['entities'] = get_redis(RedisDbs.REVIEWS).info()[f'db{RedisDbs.REVIEWS.value}']['keys']
    stats['redis']['games']['entities'] = get_redis(RedisDbs.GAMES).info()[f'db{RedisDbs.GAMES.value}']['keys']
    stats['redis']['authors']['entities'] = get_redis(RedisDbs.AUTHORS).info()[f'db{RedisDbs.AUTHORS.value}']['keys']

    stats['mongodb']['reviews']['entities'] = mongodb.reviews.estimated_document_count()
    stats['mongodb']['games']['entities'] = mongodb.games.estimated_document_count()
    stats['mongodb']['authors']['entities'] = mongodb.authors.estimated_document_count()

    return stats
