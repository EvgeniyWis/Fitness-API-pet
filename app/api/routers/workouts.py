from fastapi import APIRouter, HTTPException
from datetime import date
from app.schemas.workout import Workout, WorkoutCreate, GymType
from app.services.workout_service import workout_service

router = APIRouter()


@router.post("", response_model=Workout, status_code=201)
async def create_workout(workout_data: WorkoutCreate) -> Workout:
    """Создать новую тренировочную сессию"""
    return workout_service.create_workout(workout_data)


@router.get("", response_model=list[Workout])
async def get_workouts(
    type: GymType | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
    page: int = 1,
    size: int = 10,
) -> list[Workout]:
    """Получить список тренировок с поддержкой фильтрации"""
    return workout_service.get_workouts(
        type=type,
        date_from=date_from,
        date_to=date_to,
        min_duration=min_duration,
        max_duration=max_duration,
        page=page,
        size=size,
    )


@router.get("/{workout_id}", response_model=Workout)
async def get_workout(workout_id: int) -> Workout:
    """Получить конкретную тренировку по ID"""
    workout = workout_service.get_workout_by_id(workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.put("/{workout_id}", response_model=Workout)
async def update_workout(workout_id: int, workout_data: WorkoutCreate) -> Workout:
    """Обновить тренировку"""
    workout = workout_service.update_workout(workout_id, workout_data)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.delete("/{workout_id}", status_code=204)
async def delete_workout(workout_id: int) -> None:
    """Удалить тренировку"""
    success = workout_service.delete_workout(workout_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Workout not found")

