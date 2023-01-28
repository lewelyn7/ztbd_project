import redis
from app.core.config import settings
from enum import Enum

from redis.commands.search.field import TextField, NumericField, TagField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import NumericFilter, Query
from redis import exceptions

class RedisDbs(Enum):
    AUTHORS = 0
    GAMES = 0
    REVIEWS = 0

redisInstanceAuthors = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.AUTHORS.value)
redisInstanceGames = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.GAMES.value)
redisInstanceReviews = redis.Redis(settings.REDIS_HOST, settings.REDIS_PORT, db=RedisDbs.REVIEWS.value)
schema = (TextField("$.author_id", as_name="author_id"),TextField("$.game_id", as_name="game_id"))
try:
    info = redisInstanceReviews.ft('reviews_idx').info()
except exceptions.ResponseError as e:
    print("adding index")
    redisInstanceReviews.ft('reviews_idx').create_index(schema, definition=IndexDefinition(prefix=["review:"], index_type=IndexType.JSON))


def get_redis(db: RedisDbs) -> redis.Redis:
    if db == RedisDbs.AUTHORS:
        return redisInstanceAuthors
    elif db == RedisDbs.GAMES:
        return redisInstanceGames
    elif db == RedisDbs.REVIEWS:
        return redisInstanceReviews
    else:
        raise ValueError("no such db in redis")