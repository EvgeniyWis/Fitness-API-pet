from app.core.config import settings
from app.core.redis import get_redis
from app.security.token import hash_token
from app.models.refresh_token import RefreshToken, RefreshToken
from datetime import datetime, timedelta
from typing import Optional
import json


class JWTTokensRepository:
    """Репозиторий для работы с JWT токенами (только CRUD операции)"""

    def _get_redis_key(self, token_hash: str) -> str:
        """Получить ключ Redis для токена"""
        return f"refresh_token:{token_hash}"

    def _serialize_refresh_token(self, user_id: int, token_hash: str, expires_at: datetime, created_at: datetime, revoked: bool) -> dict:
        """Сериализация данных refresh токена для хранения в Redis"""
        return {
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": expires_at.isoformat(),
            "created_at": created_at.isoformat(),
            "revoked": revoked
        }

    def _deserialize_refresh_token(self, data: dict) -> RefreshToken:
        """Десериализация данных refresh токена из Redis"""
        return RefreshToken(
            user_id=data["user_id"],
            token_hash=data["token_hash"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            revoked=data.get("revoked", False)
        )

    # Создание refresh токена
    def create_refresh_token(self, user_id: int, token: str) -> RefreshToken:
        """Создание refresh токена"""
        redis = get_redis()
        token_hash = hash_token(token)
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        
        # Сериализуем данные
        token_data = self._serialize_refresh_token(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=created_at,
            revoked=False
        )
        
        # Сохраняем в Redis
        redis_key = self._get_redis_key(token_hash)
        redis.setex(
            redis_key,
            int((expires_at - created_at).total_seconds()),
            json.dumps(token_data)
        )
        
        # Возвращаем объект RefreshToken
        return RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=created_at,
            revoked=False
        )

    # Получение refresh токена по хешу
    def get_refresh_token_by_hash(self, token: str) -> Optional[RefreshToken]:
        """Получение refresh токена по хешу токена"""
        redis = get_redis()
        token_hash = hash_token(token)
        redis_key = self._get_redis_key(token_hash)
        
        # Получаем данные из Redis
        token_data_str = redis.get(redis_key)
        
        if not token_data_str:
            return None
        
        # Десериализуем данные
        token_data = json.loads(token_data_str)
        return self._deserialize_refresh_token(token_data)

    # Обновление статуса revoked для refresh токена
    def update_refresh_token_revoked(self, token: str, revoked: bool = True) -> bool:
        """Обновление статуса revoked для refresh токена"""
        redis = get_redis()
        token_hash = hash_token(token)
        redis_key = self._get_redis_key(token_hash)
        
        # Получаем данные из Redis
        token_data_str = redis.get(redis_key)
        
        if not token_data_str:
            return False
        
        # Десериализуем данные
        token_data = json.loads(token_data_str)
        
        # Обновляем статус revoked
        token_data["revoked"] = revoked
        
        # Получаем TTL текущего ключа
        ttl = redis.ttl(redis_key)
        
        # Если TTL отрицательный (ключ не имеет TTL), устанавливаем его на основе expires_at
        if ttl < 0:
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            now = datetime.now()
            ttl = int((expires_at - now).total_seconds())
            if ttl < 0:
                ttl = 0
        
        # Сохраняем обновленные данные
        redis.setex(redis_key, ttl, json.dumps(token_data))
        
        return True

# Глобальный экземпляр репозитория
jwt_tokens_repository = JWTTokensRepository()

