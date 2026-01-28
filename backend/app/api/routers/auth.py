import logging

from fastapi import (  # Depends - механизм Dependency Injection для переиспользования логики
    APIRouter,
    Request,
    Response,
)
from pydantic import BaseModel

from app.core.config import settings
from app.models.user import User
from app.security.cookie_utils import delete_cookie, get_cookie, set_cookie
from app.security.create_jwt_token import create_jwt_token
from app.security.get_user_id_by_token import get_user_id_by_token
from app.services.auth_service import auth_service
from app.services.jwt_tokens_service import jwt_tokens_service

router = APIRouter()
logger = logging.getLogger(__name__)


class LoginRequest(BaseModel):
    """Тело запроса на вход"""

    username: str
    password: str


@router.post("/register")
async def register(user_data: User):
    """Регистрация нового пользователя"""
    result = auth_service.register(user_data)
    logger.info("Регистрация успешна: username=%s", user_data.username)
    return result


@router.post("/login")
async def login(credentials: LoginRequest, response: Response):
    """Авторизация пользователя"""
    tokens = await auth_service.login(credentials.username, credentials.password)

    if tokens:
        access_token, refresh_token = tokens
        set_cookie(
            response, access_token, "access_token", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        set_cookie(
            response, refresh_token, "refresh_token", settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
        )
        logger.info("Вход успешен: username=%s", credentials.username)
        return {
            "message": "Успешный вход в систему",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    logger.warning("Вход отклонён: username=%s, причина=неверные учётные данные", credentials.username)
    return {"message": "Неверные учетные данные"}


@router.post("/logout")
async def logout(request: Request, response: Response):
    """Выход из системы (удаление токена из куки)"""
    # Инвалидируем Refresh токен
    refresh_token = await get_cookie(request, "refresh_token")
    if refresh_token:
        jwt_tokens_service.invalidate_refresh_token(refresh_token)

    # Инвалидируем Access токен
    access_token = await get_cookie(request, "access_token")
    if access_token:
        jwt_tokens_service.invalidate_access_token(access_token)

    # Удаляем токены из куки
    delete_cookie(response, "access_token")
    delete_cookie(response, "refresh_token")

    # Возвращаем сообщение об успешности выхода из системы
    return {"message": "Успешный выход из системы"}


@router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    """Обновление Access токена"""
    refresh_token = await get_cookie(request, "refresh_token")

    if not refresh_token:
        return {"message": "Refresh токен не найден в cookies"}

    # Проверяем не истёк ли Refresh токен
    if jwt_tokens_service.check_refresh_token_expired(refresh_token):
        return {"message": "Refresh токен истёк или инвалидирован"}

    # Получаем user_id из refresh токена
    user_id = get_user_id_by_token(refresh_token)

    # Получаем Access токен по Refresh токену
    access_token = await jwt_tokens_service.get_access_token_by_refresh_token(
        user_id, refresh_token
    )

    # Инвалидируем Refresh токен
    jwt_tokens_service.invalidate_refresh_token(refresh_token)

    # Обновляем Refresh токен
    new_refresh_token_str = create_jwt_token(user_id, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    jwt_tokens_service.create_refresh_token(user_id, new_refresh_token_str)
    set_cookie(
        response, new_refresh_token_str, "refresh_token", settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60
    )

    if access_token:
        return {"access_token": access_token, "refresh_token": new_refresh_token_str}
    else:
        return {"message": "Неверный Refresh токен"}
