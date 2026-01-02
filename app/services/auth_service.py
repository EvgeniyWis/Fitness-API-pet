# Сервис для аутентификации и авторизации
from app.repositories.auth_repository import auth_repository
from app.models.user import User
from app.security.password import hash_password
from app.security.create_jwt_token import create_jwt_token
from app.core.config import settings
from app.services.jwt_tokens_service import jwt_tokens_service


class AuthService:
    """Сервис для бизнес-логики аутентификации"""
    def register(self, user_data: User) -> User:
        """Зарегистрировать нового пользователя"""
        # Хешируем пароль перед сохранением
        user_data.password = hash_password(user_data.password)
        return auth_repository.register(user_data)

    async def login(self, username: str, password: str) -> tuple[str, str] | None:
        """Вход в систему"""
        # Получаем пользователя по username и проверяем пароль
        user: User | None = auth_repository.login(username, password)

        # Генерируем Refresh токен
        refresh_token = create_jwt_token(user.id, settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        # Сохраняем Refresh токен в БД
        jwt_tokens_service.create_refresh_token(user.id, refresh_token)

        # Генерируем Access токен
        access_token = await jwt_tokens_service.get_access_token_by_refresh_token(user.id, refresh_token)
        
        return access_token, refresh_token


# Глобальный экземпляр сервиса
auth_service = AuthService()
