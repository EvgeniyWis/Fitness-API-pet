from typing import Literal, Optional
from datetime import date
from sqlmodel import SQLModel, Column, Field
from sqlalchemy import JSON, String, Date

GymType = Literal["gym", "volleyball"]

class Workout(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    type: GymType = Field(sa_type=String) 
    duration: int = Field()
    repetitions: int = Field()
    planned_date: Optional[date] = Field(sa_type=Date)
    notes: Optional[str] = Field()
    exercises: Optional[list[str]] = Field(default_factory=list, sa_column=Column(JSON))
