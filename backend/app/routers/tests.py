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
from app.databases.sql import get_session, Session
from app.models.review.review import ReviewDB
from app.models.game.game import GameDB
from app.models.author.author import AuthorDB, AuthorCreate
from random import random
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
        result = common_settings.reviews_dao.search({"author_id": "not exists"})
        end = time.time()
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/1", response_model=SingleDbResult)
def test_case1(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"language": "not exists"})
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/2", response_model=SingleDbResult)
def test_case2(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        result = common_settings.authors_dao.save(AuthorCreate(
            id=f"idx{random():2.8f}",
            num_of_games_owned=1,
            num_reviews=10,
            playtime_forever=120,
            playtime_last_two_weeks=234,
        ))
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/3", response_model=SingleDbResult)
def test_case3(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float] = []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"content": "The"})
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/4", response_model=SingleDbResult)
def test_case4(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float] = []
    for i in range(iterations):
        start = time.time()
        result = common_settings.reviews_dao.search({"votes_funny": 12342342})
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)
    
@router.get("/5", response_model=SingleDbResult)
def test_case5(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        author: AuthorCreate = AuthorCreate(
            id=f"idx{random():2.8f}",
            num_of_games_owned=1,
            num_reviews=10,
            playtime_forever=120,
            playtime_last_two_weeks=234,
        )
        common_settings.authors_dao.save(author)
        start = time.time()
        common_settings.authors_dao.delete(author.id)
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/6", response_model=SingleDbResult)
def test_case6(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        author: AuthorCreate = AuthorCreate(
            id=f"idx{random():2.8f}",
            num_of_games_owned=1,
            num_reviews=10,
            playtime_forever=120,
            playtime_last_two_weeks=234,
        )
        common_settings.authors_dao.save(author)
        common_settings.authors_dao.delete(author.id)
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/7", response_model=SingleDbResult)
def test_case7(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        common_settings.authors_dao.delete(f"idx{random():2.8f}")
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/8", response_model=SingleDbResult)
def test_case8(iterations: int, common_settings: CommonSettings = Depends(get_common_settings)):
    times: t.List[float]= []
    for i in range(iterations):
        start = time.time()
        author: AuthorCreate = AuthorCreate(
            id=f"idx{random():2.8f}",
            num_of_games_owned=1,
            num_reviews=10,
            playtime_forever=120,
            playtime_last_two_weeks=234,
        )
        common_settings.reviews_dao.search({"author_id": author.id})
        common_settings.authors_dao.delete(author.id)
        common_settings.authors_dao.save(author)
        common_settings.reviews_dao.search({"author_id": author.id})
        common_settings.authors_dao.delete(author.id)
        end = time.time()        
        time_in_ms = (end - start) * 1000
        times.append(time_in_ms)

    return SingleDbResult(times=times)

@router.get("/stats")
def get_stats(sql_session: Session = Depends(get_session)):
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
    stats['postgresql']['reviews']['entities'] = sql_session.query(ReviewDB).count()
    stats['postgresql']['games']['entities'] = sql_session.query(GameDB).count()
    stats['postgresql']['authors']['entities'] = sql_session.query(AuthorDB).count()

    stats['redis']['reviews']['entities'] = get_redis(RedisDbs.REVIEWS).info()[f'db{RedisDbs.REVIEWS.value}']['keys']
    # stats['redis']['games']['entities'] = get_redis(RedisDbs.GAMES).info()[f'db{RedisDbs.GAMES.value}']['keys']
    # stats['redis']['authors']['entities'] = get_redis(RedisDbs.AUTHORS).info()[f'db{RedisDbs.AUTHORS.value}']['keys']

    stats['mongodb']['reviews']['entities'] = mongodb.reviews.estimated_document_count()
    stats['mongodb']['games']['entities'] = mongodb.games.estimated_document_count()
    stats['mongodb']['authors']['entities'] = mongodb.authors.estimated_document_count()

    return stats
