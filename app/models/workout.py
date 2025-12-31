from typing import Literal, Optional
from datetime import date
from sqlmodel import SQLModel, Column, Field
from sqlalchemy import JSON, String, Date
from pydantic import field_validator

GymType = Literal["gym", "volleyball"]

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    type: GymType = Field(sa_type=String) 
    duration: int = Field()
    repetitions: int = Field()
    planned_date: Optional[date] = Field(sa_type=Date)
    notes: Optional[str] = Field()
    exercises: Optional[list[str]] = Field(default_factory=list, sa_column=Column(JSON))
    
    @field_validator('planned_date', mode='before')
    @classmethod
    def convert_planned_date(cls, v):
        """Автоматически конвертировать строку в date для planned_date"""
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v
