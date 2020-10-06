from typing import List

from fastapi import HTTPException, status

from activities.dao import activity_dao
from main import app
from activities.models import Activity


@app.get("/activities", response_model=List[Activity], tags=["activities"])
def activities_list():
    return activity_dao.list()


@app.get("/activities/{_id}", response_model=Activity, tags=["activities"])
def get_activity(_id: str):
    val = activity_dao.get(_id)
    if val is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return val


@app.post("/activities", response_model=Activity, tags=["activities"])
def create_activity(activity: Activity):
    return activity_dao.save(activity)
