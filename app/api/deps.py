from fastapi import Depends, Request, HTTPException, status
from app.security.get_user_id_by_token import get_user_id_by_token
from app.services.user_service import user_service
from app.services.jwt_tokens_service import jwt_tokens_service
from app.models.user import User, UserRole

async def get_current_user_from_cookie(request: Request):
    """Получение текущего пользователя по JWT-токену из куки"""
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не найден в куки. Необходима авторизация."
        )
    
    # Проверяем не истёк ли Access токен и не инвалидирован ли он
    if jwt_tokens_service.check_access_token_expired(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access токен истёк или инвалидирован"
        )
    
    user_id = get_user_id_by_token(token)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user


def require_role(user: User) -> bool:
    """Проверяет, является ли пользователь админом. Возвращает False, если не админ."""
    return user.role == UserRole.ADMIN


async def get_current_admin_user_from_cookie(current_user: User = Depends(get_current_user_from_cookie)):
    """Получение текущего пользователя с проверкой прав администратора из куки"""
    if not require_role(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа. Требуется роль администратора."
        )
    return current_user