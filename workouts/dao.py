from connection import Dao, db, WorkoutDao
from workouts.models import Workout, Exercise

workout_dao = WorkoutDao(db.workouts, Workout)
exercise_dao = Dao[Exercise](db.exercises, Exercise)
