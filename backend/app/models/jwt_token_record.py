"""Модель таблицы БД для хранения JWT токенов (используется при REDIS_ENABLED=false)."""

from datetime import datetime
from typing import Literal

from sqlalchemy import Boolean, DateTime, String
from sqlmodel import Field, SQLModel

TokenType = Literal["refresh_token", "access_token"]


class JWTTokenRecord(SQLModel, table=True):
    """Запись JWT токена в БД."""

    __tablename__ = "jwt_token_record"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token_type: str = Field(sa_type=String(20), index=True)
    token_hash: str = Field(unique=True, index=True, sa_type=String(256))
    expires_at: datetime = Field(sa_type=DateTime)
    created_at: datetime = Field(sa_type=DateTime)
    revoked: bool = Field(default=False, sa_type=Boolean)
