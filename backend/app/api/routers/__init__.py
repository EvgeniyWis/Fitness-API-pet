from fastapi import APIRouter

from app.api.routers import auth, stats, workouts

api_router = APIRouter()

api_router.include_router(workouts.router, prefix="/workouts", tags=["workouts"])
api_router.include_router(stats.router, prefix="/stats", tags=["stats"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
