from fastapi import Request, Response

from app.core.config import settings


def set_cookie(response: Response, value: str, key: str, max_age: int) -> None:
    """
    Устанавливает токен в HTTP-only cookie

    Args:
        response: FastAPI Response объект
        token: токен для установки в cookie
    """
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,  # Защита от XSS атак
        secure=settings.COOKIE_SECURE,  # False на localhost (HTTP)
        samesite="lax",  # Защита от CSRF атак
        max_age=max_age,  # Время жизни в секундах
    )


def delete_cookie(response: Response, key: str) -> None:
    """
    Удаляет токен из cookie

    Args:
        response: FastAPI Response объект
    """
    response.delete_cookie(key=key)


async def get_cookie(request: Request, key: str) -> str | None:
    """
    Получает значение токена из cookie

    Args:
        request: FastAPI Request объект
        key: ключ токена
    """
    return request.cookies.get(key)
