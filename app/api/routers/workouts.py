from datetime import date

from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user_from_cookie
from app.models.user import User
from app.models.workout import GymType, Workout
from app.services.workout_service import workout_service

router = APIRouter()


@router.post("", response_model=Workout, status_code=201)
async def create_workout(
    workout_data: Workout, current_user: User = Depends(get_current_user_from_cookie)
) -> Workout:
    """Создать новую тренировочную сессию"""
    workout_data.user_id = current_user.id
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
    current_user: User = Depends(get_current_user_from_cookie),
) -> list[Workout]:
    """Получить список тренировок с поддержкой фильтрации"""
    return workout_service.get_workouts(
        user_id=current_user.id,
        type=type,
        date_from=date_from,
        date_to=date_to,
        min_duration=min_duration,
        max_duration=max_duration,
        page=page,
        size=size,
    )


@router.get("/{workout_id}", response_model=Workout)
async def get_workout(
    workout_id: int, current_user: User = Depends(get_current_user_from_cookie)
) -> Workout:
    """Получить конкретную тренировку по ID"""
    workout = workout_service.get_workout_by_id(workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return workout


@router.put("/{workout_id}", response_model=Workout)
async def update_workout(
    workout_id: int,
    workout_data: Workout,
    current_user: User = Depends(get_current_user_from_cookie),
) -> Workout:
    """Обновить тренировку"""
    existing_workout = workout_service.get_workout_by_id(workout_id)
    if not existing_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if existing_workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    workout = workout_service.update_workout(workout_id, workout_data)

    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")

    return workout


@router.delete("/{workout_id}", status_code=204)
async def delete_workout(
    workout_id: int, current_user: User = Depends(get_current_user_from_cookie)
) -> None:
    """Удалить тренировку"""
    existing_workout = workout_service.get_workout_by_id(workout_id)
    if not existing_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    if existing_workout.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    success = workout_service.delete_workout(workout_id)

    if not success:
        raise HTTPException(status_code=404, detail="Workout not found")
