from passlib.context import CryptContext

# Создаем контекст для работы с bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хеширует пароль используя bcrypt через passlib.
    
    Args:
        password: Пароль в открытом виде
        
    Returns:
        Хешированный пароль
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля его хешу.
    
    Args:
        plain_password: Пароль в открытом виде
        hashed_password: Хешированный пароль из базы данных
        
    Returns:
        True если пароль соответствует хешу, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)