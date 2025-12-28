from typing import Literal

from pydantic import BaseModel

GymType = Literal["gym", "volleyball"]

class WorkoutCreate(BaseModel):
    type: GymType
    duration: int
    repetitions: int

class Workout(WorkoutCreate):
    id: int
