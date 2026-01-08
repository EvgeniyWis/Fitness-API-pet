import logging
import time

from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next):
    """
    Middleware для логирования всех HTTP-запросов.

    Логирует:
    - Метод запроса
    - URL
    - IP адрес клиента
    - Время выполнения запроса
    - Статус код ответа
    - Размер ответа (если доступен)
    """
    # Засекаем время начала обработки запроса
    start_time = time.time()

    # Получаем информацию о запросе
    method = request.method
    url = str(request.url)

    # Логируем входящий запрос
    logger.info(f"→ {method} {url}")

    try:
        # Выполняем запрос
        response: Response = await call_next(request)

        # Вычисляем время выполнения
        process_time = time.time() - start_time

        # Получаем статус код
        status_code = response.status_code

        # Определяем уровень логирования в зависимости от статус кода
        if status_code >= 500:
            log_level = logging.ERROR
        elif status_code >= 400:
            log_level = logging.WARNING
        else:
            log_level = logging.INFO

        # Формируем сообщение лога
        log_message = f"← {method} {url} | Status: {status_code} | Time: {process_time:.3f}s"

        # Логируем ответ
        logger.log(log_level, log_message)

        return response

    except Exception as e:
        # Логируем ошибки, которые произошли во время обработки запроса
        process_time = time.time() - start_time
        logger.error(
            f"✗ {method} {url} | Error: {str(e)} | Time: {process_time:.3f}s", exc_info=True
        )
        # Пробрасываем исключение дальше
        raise
