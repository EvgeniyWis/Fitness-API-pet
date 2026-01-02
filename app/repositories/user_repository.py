from app.models.user import User
from app.utils.db_decorator import with_db_session
from sqlalchemy.orm import Session


class UserRepository:
    """Репозиторий для работы с пользователями (пока в памяти)"""
    @with_db_session()
    def get_user_by_id(self, db: Session, user_id: int) -> User:
        """Получение пользователя по ID"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.expunge(user)
        return user

    @with_db_session()
    def get_user_by_username(self, db: Session, username: str) -> User:
        """Получение пользователя по username"""
        user = db.query(User).filter(User.username == username).first()
        if user:
            db.expunge(user)
        return user


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
user_repository = UserRepository()

