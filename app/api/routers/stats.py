from fastapi import APIRouter
from app.services.stats_service import stats_service
from app.models.workout import GymType
from datetime import date

router = APIRouter()


@router.get("")
async def get_stats(type: GymType | None = None, date: date | None = None):
    """Получить статистику по тренировкам"""
    # Получаем статистику
    global_trains_amount = stats_service.get_global_trains_amount()
    global_trains_duration = stats_service.get_global_trains_duration()
    global_trains_by_type = stats_service.get_global_trains_by_type(type)
    global_trains_by_date = stats_service.get_global_trains_by_date(date)

    # Формируем результат
    result = {
        "global_trains_amount": global_trains_amount,
        "global_trains_duration": global_trains_duration,
    }

    # Добавляем статистику по типу, если она есть
    if type:
        result["global_trains_by_type"] = global_trains_by_type

    # Добавляем статистику по дате, если она есть
    if date:
        result["global_trains_by_date"] = global_trains_by_date

    return result


