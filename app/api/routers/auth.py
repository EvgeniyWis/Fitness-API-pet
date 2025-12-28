from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
async def register():
    """Регистрация нового пользователя"""
    # TODO: Реализовать регистрацию
    pass


@router.post("/login")
async def login():
    """Авторизация пользователя"""
    # TODO: Реализовать вход и возврат JWT-токена
    pass

