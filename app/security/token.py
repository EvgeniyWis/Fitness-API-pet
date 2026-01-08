import hashlib

from app.core.config import settings


def hash_token(token: str) -> str:
    """Хеширование токена"""
    return hashlib.sha256(f"{token}{settings.SECRET_KEY}".encode()).hexdigest()


def verify_token(token: str, hash: str) -> bool:
    """Проверка токена"""
    return hash_token(token) == hash
