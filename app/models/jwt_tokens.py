from datetime import datetime
from typing import Literal

from pydantic import BaseModel

TokenType = Literal["refresh_token", "access_token"]


class JWTToken(BaseModel):
    """Универсальный класс для представления данных JWT токена из Redis"""

    id: int | None = None
    user_id: int
    token_type: TokenType
    token_hash: str
    expires_at: datetime
    created_at: datetime
    revoked: bool = False
