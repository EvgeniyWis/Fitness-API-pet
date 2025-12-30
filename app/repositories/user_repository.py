from app.schemas.user import User
from app.repositories import users


class UserRepository:
    """Репозиторий для работы с пользователями (пока в памяти)"""
    
    def __init__(self):
        pass
    
    def get_user_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID"""
        return next((user for user in users if user.id == user_id), None)


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
user_repository = UserRepository()

