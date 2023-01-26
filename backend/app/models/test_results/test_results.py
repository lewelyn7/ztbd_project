from pydantic import BaseModel
import typing as t

class SingleDbResult(BaseModel):
    times: t.List[float]

class Result(BaseModel):
    mongodb: SingleDbResult
    postgresql: SingleDbResult
    redis: SingleDbResult



