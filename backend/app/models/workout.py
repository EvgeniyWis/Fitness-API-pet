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
    duration: int = Field(ge=1, description="Длительность в минутах, не менее 1")
    repetitions: int = Field(ge=0, description="Количество повторений, не менее 0")
    planned_date: date | None = Field(sa_type=Date)
    notes: str | None = Field()
    exercises: list[str] | None = Field(default_factory=list, sa_column=Column(JSON))

    @field_validator("planned_date", mode="before")
    @classmethod
    def convert_planned_date(cls, v):
        """Автоматически конвертировать строку в date для planned_date. Пустая строка → None."""
        if isinstance(v, str):
            s = v.strip()
            return date.fromisoformat(s)
        return v
