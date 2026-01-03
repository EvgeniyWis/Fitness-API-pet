from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum
import sqlalchemy as sa


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field()
    role: UserRole = Field(
        default=UserRole.USER,
        sa_column=sa.Column(
            sa.Enum('admin', 'user', name='userrole', native_enum=False),
            nullable=False
        )
    )