from datetime import datetime
from typing import List

from fastapi import HTTPException, status

from main import app
from workouts.dao import workout_dao
from workouts.models import Workout


@app.get("/workouts", response_model=List[Workout], tags=["workouts"])
def workouts_list():
    return workout_dao.list()


@app.get("/workouts/{_id}", response_model=Workout, tags=["workouts"])
def get_workout(_id: str):
    val = workout_dao.get(_id)
    if val is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return val


@app.post("/workouts", response_model=Workout, tags=["workouts"])
def create_workout(workout: Workout):
    workout.created_at = datetime.now()
    return workout_dao.save(workout)
