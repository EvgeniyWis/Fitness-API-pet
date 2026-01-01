from typing import Optional
from datetime import date
from app.models.workout import Workout, GymType
from app.repositories.workout_repository import workout_repository


def filter_workouts(
    workouts: list[Workout],
    user_id: int,
    type: GymType | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
    page: int = 1,
    size: int = 10,
) -> list[Workout]:
    """
    Фильтрует список тренировок по заданным параметрам.
    
    Args:
        workouts: Список тренировок для фильтрации
        type: Тип тренировки
        date_from: Начальная дата (включительно)
        date_to: Конечная дата (включительно)
        min_duration: Минимальная длительность
        max_duration: Максимальная длительность
        page: Номер страницы
        size: Количество элементов на странице
    
    Returns:
        Отфильтрованный список тренировок
    """
    result_list = list(workouts)
    page -= 1
    paged_result_list = result_list[page * size:(page + 1) * size]
    
    filters = [
        (user_id, lambda x: x.user_id == user_id),
        (type, lambda x: x.type == type),
        (date_from, lambda x: x.planned_date is not None and date_from <= x.planned_date),
        (date_to, lambda x: x.planned_date is not None and x.planned_date <= date_to),
        (min_duration, lambda x: x.duration is not None and x.duration >= min_duration),
        (max_duration, lambda x: x.duration is not None and x.duration <= max_duration),
    ]
    
    for condition, filter_func in filters:
        if condition is not None:
            paged_result_list = list(filter(filter_func, paged_result_list))
    
    return paged_result_list


class WorkoutService:
    """Сервис для бизнес-логики тренировок"""
    
    def __init__(self, repository=workout_repository):
        self.repository = repository
    
    def create_workout(self, workout_data: Workout, user_id: int) -> Workout:
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
        all_workouts = self.repository.get_all()
        return filter_workouts(
            all_workouts,
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

