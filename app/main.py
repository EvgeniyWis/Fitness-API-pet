from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import init_db
from app.core.redis import init_redis, close_redis
from app.api.routers import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Управление жизненным циклом приложения.
    Инициализирует ресурсы при старте и закрывает их при завершении.
    """
    # Инициализация при старте
    init_db()
    init_redis()
    
    yield
    
    # Закрытие при завершении
    close_redis()


def create_app() -> FastAPI:
    """Фабрика для создания FastAPI приложения"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="REST API для трекинга тренировок в тренажерном зале и волейболе",
        lifespan=lifespan,
    )
    
    # Подключаем роутеры
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    return app


app = create_app()

