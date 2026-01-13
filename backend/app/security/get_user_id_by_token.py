import jwt
from fastapi import HTTPException, status
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from app.core.config import settings


def get_user_id_by_token(token: str) -> int:
    """Получение ID пользователя по JWT-токену"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Невалидный токен: отсутствует user_id",
            )
        return user_id
    except ExpiredSignatureError as err:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек") from err
    except InvalidTokenError as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен"
        ) from err
