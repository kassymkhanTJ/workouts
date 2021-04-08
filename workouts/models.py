from datetime import datetime
from typing import List, Dict, Any, Optional, Type

from bson import ObjectId
from fastapi import Body
from pydantic import BaseModel, Field, validator, Schema


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


class Exercise(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    created_at: Optional[datetime]
    name: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    @staticmethod
    def from_db(**kwargs):
        kwargs["_id"] = str(kwargs["_id"])
        return Exercise(**kwargs)


class RoundIn(BaseModel):
    duration_seconds: int = Field(
        title='Duration',
        description='Round duration in seconds',
        gte=0,
        lt=60 * 60,
    )
    rest_seconds: \
        int = Field(
        title='Rest',
        description='Rest duration in seconds',
        gte=0,
        lt=60 * 60,
    )
    iterations: int = Field(
        title='Iterations',
        description='Number of iterations(ignored if duration_seconds != 0)',
        gte=0,
    )
    exercise_id: PyObjectId


class Round(RoundIn):
    exercise: Optional[Exercise]


class TrainingSetIn(BaseModel):
    rounds: List[RoundIn]


class TrainingSet(TrainingSetIn):
    rounds: List[Round]


class WorkoutIn(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    created_at: Optional[datetime]
    version: int
    training_sets: List[TrainingSetIn]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }


class Workout(WorkoutIn):
    training_sets: List[TrainingSet]


class WorkoutProgram(BaseModel):
    workouts: List[Workout]
