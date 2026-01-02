from app.models.user import User
from app.utils.db_decorator import with_db_session
from app.security.password import verify_password
from sqlalchemy.orm import Session
from app.repositories.user_repository import user_repository


class AuthRepository:
    """Репозиторий для работы с аутентификацией"""
    @with_db_session()
    def register(self, db: Session, user_data: User) -> User:
        """Зарегистрировать нового пользователя"""
        # Проверяем, существует ли пользователь с таким username
        if user_repository.get_user_by_username(user_data.username):
            return {"message": "Пользователь с таким username уже существует"}

        # Создаем нового пользователя
        user = User(
            **user_data.model_dump(exclude={'id'})
        )
        db.add(user)
        db.flush()  # Отправляем изменения в БД без коммита (коммит будет в декораторе)
        db.refresh(user)
        db.expunge(user)
        return {"message": "Пользователь успешно зарегистрирован"}

    @with_db_session()
    def login(self, db: Session, username: str, password: str) -> User | None:
        """
        Проверка учетных данных и возврат пользователя.
        
        Сначала находит пользователя по username, затем проверяет пароль
        используя verify_password для сравнения с хешем в БД.
        """
        user = db.query(User).filter(User.username == username).first()
        if user and verify_password(password, user.password):
            db.expunge(user)
            return user
        return None


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
auth_repository = AuthRepository()

