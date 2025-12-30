from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.security.get_user_id_by_token import get_user_id_by_token
from app.services.user_service import user_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Получение текущего пользователя по JWT-токену из заголовка Authorization"""
    user_id = get_user_id_by_token(token)
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


async def get_current_user_from_cookie(request: Request):
    """Получение текущего пользователя по JWT-токену из куки"""
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Токен не найден в куки. Необходима авторизация."
        )
    
    user_id = get_user_id_by_token(token)
    user = user_service.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return user