from app.models.user import User
from app.utils.db_decorator import with_db_session
from sqlalchemy.orm import Session


class AuthRepository:
    """Репозиторий для работы с аутентификацией (пока в памяти)"""
    @with_db_session()
    def register(self, db: Session, user_data: User) -> bool:
        """Зарегистрировать нового пользователя"""
        user = User(
            **user_data.model_dump(exclude={'id'})
        )
        db.add(user)
        db.flush()  # Отправляем изменения в БД без коммита (коммит будет в декораторе)
        db.refresh(user)
        db.expunge(user)
        return True

    @with_db_session()
    def login(self, db: Session, username: str, password: str) -> User | None:
        """Проверка учетных данных и возврат пользователя"""
        user = db.query(User).filter(User.username == username, User.password == password).first()
        if user:
            db.expunge(user)
            return user
        return None


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
auth_repository = AuthRepository()

