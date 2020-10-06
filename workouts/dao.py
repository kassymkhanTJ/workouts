from connection import Dao, db
from workouts.models import Workout

workout_dao = Dao(db.workouts, Workout)
