import bcrypt


def hash_password(password: str) -> str:
    """
    Хеширует пароль используя bcrypt.

    Args:
        password: Пароль в открытом виде (не должен превышать 72 байта)

    Returns:
        Хешированный пароль в виде строки
    """
    # Конвертируем пароль в байты
    password_bytes = password.encode("utf-8")

    # Генерируем соль и хешируем через bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Возвращаем в виде строки
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля его хешу.

    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль из базы данных

    Returns:
        True если пароль соответствует хешу, иначе False
    """
    # Конвертируем пароль в байты
    password_bytes = plain_password.encode("utf-8")

    # Проверяем пароль
    try:
        result = bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
        return result
    except Exception:
        return False
