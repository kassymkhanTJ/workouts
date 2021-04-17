from fastapi import FastAPI

app = FastAPI()

from workouts.paths import workouts_list
from activities.paths import activities_list
from workout_sessions.paths import workout_sessions_list
