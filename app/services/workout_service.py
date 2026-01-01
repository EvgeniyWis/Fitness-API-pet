from typing import Optional
from datetime import date
from app.models.workout import Workout, GymType
from app.repositories.workout_repository import workout_repository



class WorkoutService:
    """Сервис для бизнес-логики тренировок"""
    
    def __init__(self, repository=workout_repository):
        self.repository = repository
    
    def create_workout(self, workout_data: Workout) -> Workout:
        """Создать новую тренировку"""
        return self.repository.create(workout_data)
    
    def get_workouts(
        self,
        user_id: int,
        type: GymType | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        min_duration: int | None = None,
        max_duration: int | None = None,
        page: int = 1,
        size: int = 10,
    ) -> list[Workout]:
        """Получить список тренировок с фильтрацией"""
        return self.repository.get_all(
            user_id=user_id,
            type=type,
            date_from=date_from,
            date_to=date_to,
            min_duration=min_duration,
            max_duration=max_duration,
            page=page,
            size=size,
        )
    
    def get_workout_by_id(self, workout_id: int) -> Optional[Workout]:
        """Получить тренировку по ID"""
        return self.repository.get_by_id(workout_id)
    
    def update_workout(self, workout_id: int, workout_data: Workout) -> Optional[Workout]:
        """Обновить тренировку"""
        return self.repository.update(workout_id, workout_data)
    
    def delete_workout(self, workout_id: int) -> bool:
        """Удалить тренировку"""
        return self.repository.delete(workout_id)


# Глобальный экземпляр сервиса
workout_service = WorkoutService()

