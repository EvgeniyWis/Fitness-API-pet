from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.workout import GymType, Workout
from app.utils.db_decorator import with_db_session


class StatsRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""

    @with_db_session()
    def get_global_trains_amount(self, db: Session) -> int:
        """Получить общее количество тренировок"""
        return db.query(Workout).count()

    @with_db_session()
    def get_global_trains_duration(self, db: Session) -> int:
        """Получить общую длительность тренировок"""
        result = db.query(func.sum(Workout.duration)).scalar()
        return result

    @with_db_session()
    def get_global_trains_by_type(self, db: Session, type: GymType) -> int:
        """Получить количество тренировок по типу"""
        return db.query(Workout).filter(Workout.type == type).count()

    @with_db_session()
    def get_global_trains_by_date(self, db: Session, date: date) -> int:
        """Получить количество тренировок по дате"""
        return db.query(Workout).filter(Workout.planned_date == date).count()


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
stats_repository = StatsRepository()
