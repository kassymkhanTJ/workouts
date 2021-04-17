from connection import Dao, db, WorkoutDao
from workout_sessions.models import WorkoutSession

workout_session_dao = Dao[WorkoutSession](db.workout_sessions, WorkoutSession)
