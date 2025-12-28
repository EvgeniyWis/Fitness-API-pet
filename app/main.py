from fastapi import FastAPI
from app.core.config import settings
from app.api.routers import api_router


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="REST API для трекинга тренировок в тренажерном зале и волейболе",
    )
    
    # Подключаем роутеры
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    return app


app = create_app()

