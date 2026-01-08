from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from app.core.config import settings

# Импортируем модели, чтобы они зарегистрировались в SQLModel.metadata

# Создание engine для подключения к БД
engine = create_engine(
    settings.DATABASE_URL,  # URL подключения к базе данных
    connect_args={
        "check_same_thread": False
    },  # Для SQLite: разрешает использование одного соединения в разных потоках
    echo=False,  # Установить True для отладки SQL-запросов (логирование всех SQL-запросов)
)

# Создание фабрики сессий
SessionLocal = sessionmaker(
    autocommit=False,  # Отключение автоматической фиксации транзакций (нужно явно вызывать commit)
    autoflush=False,  # Отключение автоматической отправки изменений в БД (нужно явно вызывать flush)
    bind=engine,  # Привязка к engine для создания сессий
)

# Базовый класс для ORM моделей
Base = declarative_base()


def get_db() -> Generator[Session]:
    """
    Dependency для получения сессии БД в FastAPI роутерах.

    Использование:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_session():
    """
    Контекстный менеджер для получения сессии БД вне FastAPI роутеров.
    Автоматически коммитит изменения при успешном выполнении или откатывает при ошибке.

    Использование:
        with get_db_session() as db:
            items = db.query(Item).all()
            db.add(new_item)
            # commit вызывается автоматически при выходе из контекста
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """
    Инициализация базы данных: создание всех таблиц.
    Вызывается при старте приложения.
    """
    SQLModel.metadata.create_all(bind=engine)
