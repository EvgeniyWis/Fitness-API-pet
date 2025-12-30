from fastapi import APIRouter, Response, Depends  # Depends - механизм Dependency Injection для переиспользования логики
from app.schemas.user import UserCreate, User
from app.services.auth_service import auth_service
from app.api.deps import get_current_user_from_cookie  # Dependency для автоматической авторизации по куки
from app.security.cookie_utils import set_auth_cookie, delete_auth_cookie

router = APIRouter()


@router.post("/register")
async def register(user_data: UserCreate):
    """Регистрация нового пользователя"""
    return auth_service.register(user_data)


@router.post("/login")
async def login(username: str, password: str, response: Response):
    """Авторизация пользователя"""
    token = auth_service.login(username, password)
    
    if token:
        set_auth_cookie(response, token)
        return {"message": "Успешный вход в систему", "access_token": token}
    
    return {"message": "Неверные учетные данные"}


@router.post("/logout")
async def logout(response: Response):
    """Выход из системы (удаление токена из куки)"""
    delete_auth_cookie(response)
    return {"message": "Успешный выход из системы"}


@router.get("/me")
async def get_current_user_info(current_user: User = Depends(get_current_user_from_cookie)):
    return current_user

