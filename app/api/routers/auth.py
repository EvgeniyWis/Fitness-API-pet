from fastapi import APIRouter, Response, Request  # Depends - механизм Dependency Injection для переиспользования логики
from app.core.config import settings
from app.models.user import User
from app.services.auth_service import auth_service
from app.security.cookie_utils import set_cookie, get_cookie, delete_cookie
from app.services.jwt_tokens_service import jwt_tokens_service
from app.security.create_jwt_token import create_jwt_token
from app.security.get_user_id_by_token import get_user_id_by_token


router = APIRouter()


@router.post("/register")
async def register(user_data: User):
    """Регистрация нового пользователя"""
    return auth_service.register(user_data)


@router.post("/login")
async def login(username: str, password: str, response: Response):
    """Авторизация пользователя"""
    tokens = await auth_service.login(username, password)
    
    if tokens:
        access_token, refresh_token = tokens
        set_cookie(response, access_token, "access_token", settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        set_cookie(response, refresh_token, "refresh_token", settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)
        return {"message": "Успешный вход в систему", "access_token": access_token, "refresh_token": refresh_token}
    
    return {"message": "Неверные учетные данные"}


@router.post("/logout")
async def logout(request: Request, response: Response):
    """Выход из системы (удаление токена из куки)"""
    # Инвалидируем Refresh токен
    refresh_token = await get_cookie(request, "refresh_token")
    if refresh_token:
        jwt_tokens_service.invalidate_refresh_token(refresh_token)

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
    access_token = await jwt_tokens_service.get_access_token_by_refresh_token(user_id, refresh_token)

    # Инвалидируем Refresh токен
    jwt_tokens_service.invalidate_refresh_token(refresh_token)

    # Обновляем Refresh токен
    new_refresh_token_str = create_jwt_token(user_id, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    jwt_tokens_service.create_refresh_token(user_id, new_refresh_token_str)
    set_cookie(response, new_refresh_token_str, "refresh_token", settings.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    if access_token:
        return {"access_token": access_token, "refresh_token": new_refresh_token_str}
    else:
        return {"message": "Неверный Refresh токен"}
