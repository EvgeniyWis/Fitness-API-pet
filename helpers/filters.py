from datetime import date
from models import Workout, GymType


def filter_workouts(
    workouts: list[Workout],
    type: GymType | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
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
    
    Returns:
        Отфильтрованный список тренировок
    """
    result_list = list(workouts)
    
    filters = [
        (type, lambda x: x.type == type),
        (date_from, lambda x: x.planned_date is not None and date_from <= x.planned_date),
        (date_to, lambda x: x.planned_date is not None and x.planned_date <= date_to),
        (min_duration, lambda x: x.duration is not None and x.duration >= min_duration),
        (max_duration, lambda x: x.duration is not None and x.duration <= max_duration),
    ]
    
    for condition, filter_func in filters:
        if condition is not None:
            result_list = list(filter(filter_func, result_list))
    
    return result_list

