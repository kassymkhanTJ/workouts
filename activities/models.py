from datetime import datetime

from fastapi import Body
from pydantic import BaseModel


class Activity(BaseModel):
    created_at: datetime = Body(None)
