from fastapi import Response
from app.core.config import settings


def set_auth_cookie(response: Response, token: str) -> None:
    """
    Устанавливает JWT токен в HTTP-only cookie
    
    Args:
        response: FastAPI Response объект
        token: JWT токен для установки в cookie
    """
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,  # Защита от XSS атак
        secure=True,    # Только HTTPS (в production)
        samesite="lax", # Защита от CSRF атак
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Время жизни в секундах
    )


def delete_auth_cookie(response: Response) -> None:
    """
    Удаляет JWT токен из cookie
    
    Args:
        response: FastAPI Response объект
    """
    response.delete_cookie(key="access_token")

