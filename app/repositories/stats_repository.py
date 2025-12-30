from app.schemas.workout import GymType
from datetime import date
from app.repositories import workouts


class StatsRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""
    
    def __init__(self):
        pass
    
    def get_global_trains_amount(self) -> int:
        """Получить общее количество тренировок"""
        return len(workouts)

    def get_global_trains_duration(self) -> int:
        """Получить общую длительность тренировок"""
        return sum(workout.duration for workout in workouts)

    def get_global_trains_by_type(self, type: GymType) -> int:
        """Получить количество тренировок по типу"""
        return sum(1 for workout in workouts if workout.type == type)

    def get_global_trains_by_date(self, date: date) -> int:
        """Получить количество тренировок по дате"""
        return sum(1 for workout in workouts if workout.planned_date == date)


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
stats_repository = StatsRepository()

