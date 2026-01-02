from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Relationship
from sqlalchemy import DateTime, Boolean, String


if TYPE_CHECKING:
    from app.models.user import User


class RefreshToken(SQLModel, table=True):
    """Модель для хранения refresh токенов в БД"""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    token_hash: str = Field(sa_column=Column(String, unique=True, index=True))  # Хеш токена для безопасности
    expires_at: datetime = Field(sa_column=Column(DateTime))
    created_at: datetime = Field(sa_column=Column(DateTime))
    revoked: bool = Field(default=False, sa_column=Column(Boolean))  # Отозван ли токен
    user: "User" = Relationship(back_populates="refresh_token")
