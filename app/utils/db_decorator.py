from functools import wraps
from typing import Callable
from app.core.database import get_db_session


def with_db_session(expunge_all: bool = False):
    """
    Декоратор для автоматического управления сессией БД.
    
    Автоматически создает сессию БД, передает её как первый параметр метода (после self),
    коммитит изменения при успешном выполнении или откатывает при ошибке.
    
    Args:
        expunge_all: Если True, автоматически отсоединяет все объекты от сессии перед возвратом.
                    Полезно для методов, возвращающих объекты, которые должны быть доступны
                    после закрытия сессии.
    
    Использование:
        @with_db_session()
        def get_all(self, db: Session) -> list[Workout]:
            return db.query(Workout).all()
        
        @with_db_session(expunge_all=True)
        def get_by_id(self, db: Session, workout_id: int) -> Optional[Workout]:
            workout = db.query(Workout).filter(Workout.id == workout_id).first()
            if workout:
                db.expunge(workout)
            return workout
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            with get_db_session() as db:
                try:
                    # Вызываем функцию с сессией как первым аргументом после self
                    result = func(self, db, *args, **kwargs)
                    
                    # Если нужно отсоединить все объекты от сессии
                    if expunge_all:
                        db.expunge_all()
                    
                    return result
                except Exception:
                    # Откат уже происходит в get_db_session, но можно добавить дополнительную логику
                    raise
        
        return wrapper
    return decorator

