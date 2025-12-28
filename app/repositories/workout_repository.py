from typing import Optional
from app.schemas.workout import Workout, WorkoutCreate, GymType


class WorkoutRepository:
    """Репозиторий для работы с тренировками (пока в памяти)"""
    
    def __init__(self):
        self._workouts: list[Workout] = []
        self._next_id = 1
    
    def create(self, workout_data: WorkoutCreate) -> Workout:
        """Создать новую тренировку"""
        workout = Workout(
            id=self._next_id,
            **workout_data.model_dump()
        )
        self._next_id += 1
        self._workouts.append(workout)
        return workout
    
    def get_all(self) -> list[Workout]:
        """Получить все тренировки"""
        return self._workouts.copy()
    
    def get_by_id(self, workout_id: int) -> Optional[Workout]:
        """Получить тренировку по ID"""
        for workout in self._workouts:
            if workout.id == workout_id:
                return workout
        return None
    
    def update(self, workout_id: int, workout_data: WorkoutCreate) -> Optional[Workout]:
        """Обновить тренировку"""
        for i, workout in enumerate(self._workouts):
            if workout.id == workout_id:
                updated_workout = Workout(
                    id=workout_id,
                    **workout_data.model_dump()
                )
                self._workouts[i] = updated_workout
                return updated_workout
        return None
    
    def delete(self, workout_id: int) -> bool:
        """Удалить тренировку"""
        for i, workout in enumerate(self._workouts):
            if workout.id == workout_id:
                del self._workouts[i]
                return True
        return False


# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
workout_repository = WorkoutRepository()

