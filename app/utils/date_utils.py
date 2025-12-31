from datetime import date


def convert_date_string(date_value):
    """Преобразовать строку даты в объект date"""
    if isinstance(date_value, str):
        return date.fromisoformat(date_value)
    return date_value

