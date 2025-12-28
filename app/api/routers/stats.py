from fastapi import APIRouter

router = APIRouter()


@router.get("")
async def get_stats():
    """Получить статистику по тренировкам"""
    # TODO: Реализовать получение статистики
    pass

