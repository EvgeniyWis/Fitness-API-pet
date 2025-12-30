from app.schemas.user import UserCreate, User
from app.repositories import users


class AuthRepository:
    """Репозиторий для работы с аутентификацией (пока в памяти)"""
    
    def __init__(self):
        self._next_id = 1
        pass
    
    def register(self, user_data: UserCreate) -> User:
        """Зарегистрировать нового пользователя"""
        user = User(
            id=self._next_id,
            **user_data.model_dump()
        )
        self._next_id += 1
        users.append(user)
        return user

    def login(self, username: str, password: str) -> User | None:
        """Проверка учетных данных и возврат пользователя"""
        for user in users:
            if user.username == username and user.password == password:
                return user

        return None


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
auth_repository = AuthRepository()

