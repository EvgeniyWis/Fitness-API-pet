from datetime import date


def convert_date_string(date_value):
    """Преобразовать строку даты в объект date. Пустая строка или None → None."""
    if date_value is None:
        return None
    if isinstance(date_value, str):
        value = date_value.strip()
        if not value:
            return None
        return date.fromisoformat(value)
    return date_value
