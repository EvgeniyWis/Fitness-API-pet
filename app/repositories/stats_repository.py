from app.models.workout import GymType
from datetime import date
from app.core.database import get_db_session
from app.models.workout import Workout
from sqlalchemy import func


class StatsRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""
    def get_global_trains_amount(self) -> int:
        """Получить общее количество тренировок"""
        with get_db_session() as db:
            return db.query(Workout).count()

    def get_global_trains_duration(self) -> int:
        """Получить общую длительность тренировок"""
        with get_db_session() as db:
            result = db.query(func.sum(Workout.duration)).scalar()
            return result

    def get_global_trains_by_type(self, type: GymType) -> int:
        """Получить количество тренировок по типу"""
        with get_db_session() as db:
            return db.query(Workout).filter(Workout.type == type).count()

    def get_global_trains_by_date(self, date: date) -> int:
        """Получить количество тренировок по дате"""
        with get_db_session() as db:
            return db.query(Workout).filter(Workout.planned_date == date).count()


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
stats_repository = StatsRepository()

