from typing import Literal
from datetime import date
from pydantic import BaseModel
from typing import Optional

GymType = Literal["gym", "volleyball"]

class WorkoutCreate(BaseModel):
    type: GymType
    duration: int
    repetitions: int
    planned_date: Optional[date] = None
    notes: Optional[str] = None
    exercises: Optional[list[str]] = None

class Workout(WorkoutCreate):
    id: int
