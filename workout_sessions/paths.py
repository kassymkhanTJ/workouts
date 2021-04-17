from typing import List

from pydantic import ValidationError

from decorators.path_decorators import validate_bson_id, raise_not_found
from main import app
from workout_sessions.models import WorkoutSession, WorkoutSessionIn, FinishWorkoutSession, WorkoutSessionState
from workout_sessions.services import workout_session_service


@app.get("/workout_sessions", response_model=List[WorkoutSession], tags=["workout_sessions"])
def workout_sessions_list():
    return workout_session_service.list()


@app.get("/workout_sessions/{_id}", response_model=WorkoutSession, tags=["workout_sessions"])
@validate_bson_id
@raise_not_found
def get_workout_session(_id: str):
    return workout_session_service.get(_id)


@app.post("/workout_sessions", response_model=WorkoutSession, tags=["workout_sessions"])
def create_workout_session(workout_session: WorkoutSessionIn):
    return workout_session_service.active() or workout_session_service.create(workout_session,
                                                                              {'state': WorkoutSessionState.START})


@app.get("/workout_sessions/active/", response_model=WorkoutSession, tags=["workout_sessions"])
@raise_not_found
def get_active_workout_session():
    return workout_session_service.active()


@app.put("/workout_sessions/{_id}/finish", response_model=WorkoutSession, tags=["workout_sessions"])
@validate_bson_id
@raise_not_found
def finish_workout_session(_id: str, data: FinishWorkoutSession):
    return workout_session_service.finish_session(_id, data)
