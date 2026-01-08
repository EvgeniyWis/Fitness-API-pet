# Сервис для статистики тренировок
from datetime import date

from app.models.workout import GymType
from app.repositories.stats_repository import stats_repository


class StatsService:
    """Сервис для бизнес-логики тренировок"""

    def get_global_trains_amount(self) -> int:
        """Получить общее количество тренировок"""
        return stats_repository.get_global_trains_amount()

    def get_global_trains_duration(self) -> int:
        """Получить общую длительность тренировок"""
        return stats_repository.get_global_trains_duration()

    def get_global_trains_by_type(self, type: GymType) -> int:
        """Получить количество тренировок по типу"""
        return stats_repository.get_global_trains_by_type(type)

    def get_global_trains_by_date(self, date: date) -> int:
        """Получить количество тренировок по дате"""
        return stats_repository.get_global_trains_by_date(date)


# Глобальный экземпляр сервиса
stats_service = StatsService()
