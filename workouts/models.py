from datetime import datetime
from typing import List

from fastapi import Body
from pydantic import BaseModel, Field


class Exercise(BaseModel):
    name: str


class Round(BaseModel):
    exercise: Exercise
    duration_seconds: int = Field(
        title='Duration',
        description='Round duration in seconds',
        gte=0,
        lt=24 * 60,
    )
    rest_seconds: int = Field(
        title='Rest',
        description='Rest duration in seconds',
        gte=0,
        lt=24 * 60,
    )
    iterations: int = Field(
        title='Iterations',
        description='Number of iterations(ignored if duration_seconds != 0)',
        gte=0,
    )


class TrainingSet(BaseModel):
    rounds: List[Round]


class Workout(BaseModel):
    _id: str
    created_at: datetime = Body(None)
    training_sets: List[TrainingSet]


class WorkoutProgram(BaseModel):
    workouts: List[Workout]
