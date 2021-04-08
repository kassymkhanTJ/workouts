import functools

import bson
from fastapi import HTTPException
from starlette import status

from exceptions import ModelInstanceNotFound


def validate_bson_id(path):
    @functools.wraps(path)
    def decorator(**kwargs):
        if "_id" not in kwargs:
            return
        if not bson.objectid.ObjectId.is_valid(kwargs["_id"]):
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "_id must be valid ObjectId")
        return path(**kwargs)

    return decorator


def raise_not_found(path):
    @functools.wraps(path)
    def decorator(**kwargs):
        try:
            return path(**kwargs)
        except ModelInstanceNotFound as e:
            raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    return decorator
