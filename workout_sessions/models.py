from datetime import datetime
from enum import Enum
from typing import List, Dict, Any, Optional, Type

from bson import ObjectId
from fastapi import Body
from pydantic import BaseModel, Field, validator, Schema

from workouts.models import PyObjectId


class WorkoutSessionState(str, Enum):
    START = 'START'
    SUCCESS = 'SUCCESS'
    CANCEL = 'CANCEL'


TERMINAL_STATES = {WorkoutSessionState.SUCCESS, WorkoutSessionState.CANCEL}


class WorkoutSessionIn(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    created_at: Optional[datetime]
    workout_id: PyObjectId
    workout_version: int
    state: Optional[WorkoutSessionState] = WorkoutSessionState.START

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

    def is_terminal(self):
        return self.state and self.state in TERMINAL_STATES


class WorkoutSession(WorkoutSessionIn):
    finished_at: Optional[datetime]

    class Config:
        use_enum_values = True


class FinishWorkoutSession(BaseModel):
    state: WorkoutSessionState = Field()

    @validator('state')
    def validate_state(cls, v):
        if v not in TERMINAL_STATES:
            raise ValueError('state must be terminal')
        return v
