import jwt
from datetime import datetime, timedelta
from app.core.config import settings


def create_access_token(user_id: int) -> str:
    """
    Создает JWT токен для пользователя
    
    Args:
        user_id: ID пользователя
        
    Returns:
        JWT токен в виде строки
    """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "user_id": user_id,
        "exp": expire
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

