from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.database import init_db
from app.core.redis import init_redis, close_redis
from app.core.logging_config import setup_logging
from app.api.routers import api_router
from app.api.middleware import logging_middleware


@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Управление жизненным циклом приложения.
    Инициализирует ресурсы при старте и закрывает их при завершении.
    """
    # Инициализация при старте
    setup_logging(settings.LOG_LEVEL)
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
    
    # Подключаем middleware для логирования
    app.middleware("http")(logging_middleware)
    
    # Подключаем роутеры
    app.include_router(api_router, prefix=settings.API_PREFIX)
    
    return app


app = create_app()

