from datetime import datetime, timedelta

import jwt

from app.core.config import settings


def create_jwt_token(user_id: int, expire_minutes: int) -> str:
    """
    Создает JWT токен для пользователя

    Args:
        user_id: ID пользователя

    Returns:
        JWT токен в виде строки
    """
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    payload = {"user_id": user_id, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
