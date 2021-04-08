from typing import List

from decorators.path_decorators import validate_bson_id, raise_not_found
from main import app
from workouts.models import Workout, Exercise, WorkoutIn
from workouts.services import workout_service, exercise_service


@app.get("/workouts", response_model=List[Workout], tags=["workouts"])
def workouts_list():
    return workout_service.list()


@app.get("/workouts/{_id}", response_model=Workout, tags=["workouts"])
@validate_bson_id
@raise_not_found
def get_workout(_id: str):
    return workout_service.get(_id)


@app.post("/workouts", response_model=Workout, tags=["workouts"])
def create_workout(workout: WorkoutIn):
    return workout_service.create(workout)


@app.put("/workouts/{_id}", response_model=Workout, tags=["workouts"])
@validate_bson_id
@raise_not_found
def update_workout(_id: str, data: WorkoutIn):
    return workout_service.update(_id, data.dict())


@app.get("/exercises", response_model=List[Exercise], tags=["exercises"])
def exercise_list():
    return exercise_service.list()


@app.post("/exercises", response_model=Exercise, tags=["exercises"])
def create_exercise(exercise: Exercise):
    return exercise_service.create(exercise)
