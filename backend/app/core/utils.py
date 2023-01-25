from fastapi import status
from fastapi import HTTPException
def raise_409(func):
	
    def inner1(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            args = e.args
            if 'exists' in e.args:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT)
            else:
                raise e

    return inner1