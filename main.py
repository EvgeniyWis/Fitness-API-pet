from fastapi import FastAPI
from models import Workout, WorkoutCreate, GymType
from datetime import date
from helpers.filters import filter_workouts

app = FastAPI()

workout_list = []


@app.post("/workouts")
async def create_workout(workout_data: WorkoutCreate) -> Workout:
    workout = Workout(
        id=len(workout_list) + 1,
        **workout_data.model_dump()
    )
    workout_list.append(workout)
    return workout


@app.get("/workouts")
async def get_workouts(type: GymType | None = None, date_from: date | None = None, date_to: date | None = None, min_duration: int | None = None, max_duration: int | None = None) -> list[Workout]:
    return filter_workouts(
        workout_list,
        type=type,
        date_from=date_from,
        date_to=date_to,
        min_duration=min_duration,
        max_duration=max_duration,
    )