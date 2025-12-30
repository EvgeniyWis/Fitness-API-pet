# Сервис для аутентификации и авторизации
from app.repositories.user_repository import user_repository
from app.schemas.user import User

class UserService:
    """Сервис для бизнес-логики пользователей"""
    
    def __init__(self):
        pass
    
    def get_user_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID"""
        return user_repository.get_user_by_id(user_id)

# Глобальный экземпляр сервиса
user_service = UserService()
