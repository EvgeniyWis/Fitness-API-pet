from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.refresh_token import RefreshToken

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field()
    password: str = Field()
    refresh_token: "RefreshToken" = Relationship(back_populates="user")