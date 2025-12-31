from app.models.user import User
from app.core.database import get_db_session


class UserRepository:
    """Репозиторий для работы с пользователями (пока в памяти)"""
    def get_user_by_id(self, user_id: int) -> User:
        """Получение пользователя по ID"""
        with get_db_session() as db:
            return db.query(User).filter(User.id == user_id).first()


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
user_repository = UserRepository()

