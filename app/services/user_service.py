# Сервис для аутентификации и авторизации
from app.repositories.user_repository import user_repository
from app.models.user import User

class UserService:
    """Сервис для бизнес-логики пользователей"""
    def get_user_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID"""
        return user_repository.get_user_by_id(user_id)

# Глобальный экземпляр сервиса
user_service = UserService()
