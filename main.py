from fastapi import FastAPI
from models import Workout, WorkoutCreate

app = FastAPI()

workout_list = [
    Workout(id=1, type="gym", duration=30, repetitions=10),
    Workout(id=2, type="volleyball", duration=60, repetitions=20),
]


@app.post("/workouts")
async def create_workout(workout_data: WorkoutCreate) -> Workout:
    workout = Workout(
        id=len(workout_list) + 1,
        type=workout_data.type,
        duration=workout_data.duration,
        repetitions=workout_data.repetitions
    )
    workout_list.append(workout)
    return workout


@app.get("/workouts")
async def get_workouts() -> list[Workout]:
    return workout_list
