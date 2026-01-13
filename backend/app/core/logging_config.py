import logging
import sys
from pathlib import Path


def setup_logging(log_level: str = "INFO") -> None:
    """
    Настройка логирования для приложения.

    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    # Создаем директорию для логов, если её нет
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Настройка формата логов
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Настройка root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Очищаем существующие обработчики
    root_logger.handlers.clear()

    # Создаем общий форматтер
    formatter = logging.Formatter(log_format, date_format)
    log_level_attr = getattr(logging, log_level.upper())

    # Консольный обработчик (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level_attr)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Файловый обработчик для всех логов
    file_handler = logging.FileHandler(log_dir / "app.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    # Файловый обработчик для ошибок
    error_file_handler = logging.FileHandler(log_dir / "errors.log", encoding="utf-8")
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    root_logger.addHandler(error_file_handler)

    logging.info("Логирование настроено успешно")


def get_logger(name: str) -> logging.Logger:
    """
    Получить логгер с указанным именем.

    Args:
        name: Имя логгера (обычно __name__)

    Returns:
        Настроенный логгер
    """
    return logging.getLogger(name)
