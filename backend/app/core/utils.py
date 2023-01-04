from fastapi import status
from fastapi import HTTPException
def raise_409(func):
	
    def inner1(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    return inner1