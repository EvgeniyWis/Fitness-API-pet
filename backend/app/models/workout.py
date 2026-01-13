from datetime import date
from typing import Literal

from pydantic import field_validator
from sqlalchemy import JSON, Date, String
from sqlmodel import Column, Field, SQLModel

GymType = Literal["gym", "volleyball"]


class Workout(SQLModel, table=True):
    id: int | None = Field(primary_key=True, sa_column_kwargs={"autoincrement": True})
    user_id: int | None = Field(foreign_key="user.id")
    type: GymType = Field(sa_type=String)
    duration: int = Field()
    repetitions: int = Field()
    planned_date: date | None = Field(sa_type=Date)
    notes: str | None = Field()
    exercises: list[str] | None = Field(default_factory=list, sa_column=Column(JSON))

    @field_validator("planned_date", mode="before")
    @classmethod
    def convert_planned_date(cls, v):
        """Автоматически конвертировать строку в date для planned_date"""
        if isinstance(v, str):
            return date.fromisoformat(v)
        return v
