from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class RefreshToken(BaseModel):
    """Класс для представления данных refresh токена из Redis"""
    id: Optional[int] = None
    user_id: int
    token_hash: str
    expires_at: datetime
    created_at: datetime
    revoked: bool = False

