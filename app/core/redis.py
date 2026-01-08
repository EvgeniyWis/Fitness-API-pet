from redis import Redis

from app.core.config import settings

# Глобальный экземпляр Redis клиента
redis_client: Redis | None = None


def get_redis() -> Redis:
    """
    Получить экземпляр Redis клиента.

    Returns:
        Redis: Экземпляр клиента Redis

    Raises:
        RuntimeError: Если Redis клиент не инициализирован
    """
    if redis_client is None:
        raise RuntimeError(
            "Redis клиент не инициализирован. Вызовите init_redis() при старте приложения."
        )
    return redis_client


def init_redis() -> Redis:
    """
    Инициализировать подключение к Redis.

    Returns:
        Redis: Экземпляр клиента Redis
    """
    global redis_client

    # Собираем URL из отдельных параметров
    redis_url = f"redis://{settings.REDIS_USERNAME}:{settings.REDIS_PASSWORD}@{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"

    # Создаем клиент из URL
    redis_client = Redis.from_url(
        redis_url,
        decode_responses=True,  # Автоматически декодировать ответы в строки
        socket_connect_timeout=5,  # Таймаут подключения
        socket_timeout=5,  # Таймаут операций
        retry_on_timeout=True,  # Повторять при таймауте
    )

    # Проверяем подключение
    try:
        redis_client.ping()
        print("✓ Подключение к Redis установлено")
    except Exception as e:
        print(f"✗ Ошибка подключения к Redis: {e}")
        raise

    return redis_client


def close_redis() -> None:
    """
    Закрыть подключение к Redis.
    """
    global redis_client
    if redis_client is not None:
        redis_client.close()
        redis_client = None
        print("✓ Подключение к Redis закрыто")
