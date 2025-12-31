from app.models.user import User
from app.core.database import get_db_session


class AuthRepository:
    """Репозиторий для работы с аутентификацией (пока в памяти)"""
    def register(self, user_data: User) -> bool:
        """Зарегистрировать нового пользователя"""
        with get_db_session() as db:
            user = User(
                **user_data.model_dump(exclude={'id'})
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            db.expunge(user)
            return True

    def login(self, username: str, password: str) -> User | None:
        """Проверка учетных данных и возврат пользователя"""
        with get_db_session() as db:
            user = db.query(User).filter(User.username == username, User.password == password).first()
            if user:
                db.expunge(user)
                return user

        return None


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
auth_repository = AuthRepository()

