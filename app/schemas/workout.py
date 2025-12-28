from typing import Literal, Optional
from datetime import date
from pydantic import BaseModel


GymType = Literal["gym", "volleyball"]


class WorkoutCreate(BaseModel):
    """Схема для создания тренировки"""
    type: GymType
    duration: int
    repetitions: int
    planned_date: Optional[date] = None
    notes: Optional[str] = None
    exercises: Optional[list[str]] = None


class Workout(WorkoutCreate):
    """Схема тренировки с ID"""
    id: int

