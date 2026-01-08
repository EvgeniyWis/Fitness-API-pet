from enum import Enum

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field()
    role: UserRole = Field(
        default=UserRole.USER,
        sa_column=sa.Column(
            sa.Enum("admin", "user", name="userrole", native_enum=False), nullable=False
        ),
    )
