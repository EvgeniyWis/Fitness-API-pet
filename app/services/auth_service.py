# Сервис для аутентификации и авторизации
from app.repositories.auth_repository import auth_repository
from app.models.user import User
from app.security.hash_password import hash_password
from app.security.create_access_token import create_access_token

class AuthService:
    """Сервис для бизнес-логики тренировок"""
    def register(self, user_data: User) -> User:
        """Зарегистрировать нового пользователя"""
        # Хешируем пароль
        user_data.password = hash_password(user_data.password)
        return auth_repository.register(user_data)

    def login(self, username: str, password: str) -> str | None:
        """Вход в систему"""
        # Хешируем пароль
        password = hash_password(password)
        user = auth_repository.login(username, password)
        
        if user:
            # Генерируем JWT токен
            return create_access_token(user.id)
        
        return None


# Глобальный экземпляр сервиса
auth_service = AuthService()
