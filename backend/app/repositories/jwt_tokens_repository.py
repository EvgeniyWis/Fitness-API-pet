import json
from datetime import datetime, timedelta

from app.core.config import settings
from app.core.database import get_db_session
from app.core.redis import get_redis
from app.models.jwt_token_record import JWTTokenRecord
from app.models.jwt_tokens import JWTToken, TokenType
from app.security.token import hash_token


class JWTTokensRepository:
    """Репозиторий для работы с JWT токенами (Redis или БД при REDIS_ENABLED=false)."""

    def _get_redis_key(self, token_type: TokenType, token_hash: str) -> str:
        """Получить ключ Redis для токена"""
        return f"{token_type}:{token_hash}"

    def _serialize_token_data(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
        created_at: datetime,
        revoked: bool = False,
    ) -> dict:
        """Сериализация данных токена для хранения в Redis"""
        token_data = {
            "user_id": user_id,
            "token_hash": token_hash,
            "expires_at": expires_at.isoformat(),
            "created_at": created_at.isoformat(),
            "revoked": revoked,
        }
        return token_data

    def _deserialize_token_data(self, data: dict, token_type: TokenType) -> JWTToken:
        """Универсальная десериализация данных токена из Redis/БД"""
        return JWTToken(
            user_id=data["user_id"],
            token_type=token_type,
            token_hash=data["token_hash"],
            expires_at=datetime.fromisoformat(data["expires_at"]),
            created_at=datetime.fromisoformat(data["created_at"]),
            revoked=data.get("revoked", False),
        )

    def _deserialize_refresh_token(self, data: dict) -> JWTToken:
        """Десериализация данных refresh токена из Redis"""
        return self._deserialize_token_data(data, "refresh_token")

    def _deserialize_access_token(self, data: dict) -> JWTToken:
        """Десериализация данных access токена из Redis"""
        return self._deserialize_token_data(data, "access_token")

    def _save_token(
        self, token_type: TokenType, user_id: int, token: str, expire_minutes: int
    ) -> tuple[str, datetime, datetime]:
        """Сохранить токен в Redis или в БД (при REDIS_ENABLED=false)."""
        token_hash = hash_token(token)
        created_at = datetime.now()
        expires_at = created_at + timedelta(minutes=expire_minutes)

        if settings.REDIS_ENABLED:
            redis = get_redis()
            token_data = self._serialize_token_data(
                user_id=user_id,
                token_hash=token_hash,
                expires_at=expires_at,
                created_at=created_at,
                revoked=False,
            )
            redis_key = self._get_redis_key(token_type, token_hash)
            redis.setex(
                redis_key,
                int((expires_at - created_at).total_seconds()),
                json.dumps(token_data),
            )
        else:
            with get_db_session() as db:
                record = JWTTokenRecord(
                    user_id=user_id,
                    token_type=token_type,
                    token_hash=token_hash,
                    expires_at=expires_at,
                    created_at=created_at,
                    revoked=False,
                )
                db.add(record)
        return token_hash, created_at, expires_at

    # Создание refresh токена
    def create_refresh_token(self, user_id: int, token: str) -> JWTToken:
        """Создание refresh токена"""
        token_hash, created_at, expires_at = self._save_token(
            "refresh_token", user_id, token, settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )

        # Возвращаем объект JWTToken
        return JWTToken(
            user_id=user_id,
            token_type="refresh_token",
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=created_at,
            revoked=False,
        )

    def _get_token_data_by_hash(self, token: str, token_type: TokenType) -> dict | None:
        """Универсальный метод для получения данных токена по хешу (Redis или БД)."""
        token_hash = hash_token(token)

        if settings.REDIS_ENABLED:
            redis = get_redis()
            redis_key = self._get_redis_key(token_type, token_hash)
            token_data_str = redis.get(redis_key)
            return json.loads(token_data_str)

        with get_db_session() as db:
            row = (
                db.query(JWTTokenRecord)
                .filter(
                    JWTTokenRecord.token_hash == token_hash,
                    JWTTokenRecord.token_type == token_type,
                )
                .first()
            )
            return {
                "user_id": row.user_id,
                "token_hash": row.token_hash,
                "expires_at": row.expires_at.isoformat(),
                "created_at": row.created_at.isoformat(),
                "revoked": row.revoked,
            }

    def get_token_by_hash(self, token: str, token_type: TokenType) -> JWTToken | None:
        """Универсальный метод для получения токена по хешу"""
        token_data = self._get_token_data_by_hash(token, token_type)
        if not token_data:
            return None
        return self._deserialize_token_data(token_data, token_type)

    def _update_token_revoked(
        self, token: str, token_type: TokenType, revoked: bool = True
    ) -> bool:
        """Универсальный метод для обновления статуса revoked токена (Redis или БД)."""
        token_hash = hash_token(token)

        if settings.REDIS_ENABLED:
            redis = get_redis()
            redis_key = self._get_redis_key(token_type, token_hash)
            token_data_str = redis.get(redis_key)
            token_data = json.loads(token_data_str)
            token_data["revoked"] = revoked
            ttl = redis.ttl(redis_key)
            if ttl < 0:
                expires_at = datetime.fromisoformat(token_data["expires_at"])
                now = datetime.now()
                ttl = max(0, int((expires_at - now).total_seconds()))
            redis.setex(redis_key, ttl, json.dumps(token_data))
            return True

        with get_db_session() as db:
            row = (
                db.query(JWTTokenRecord)
                .filter(
                    JWTTokenRecord.token_hash == token_hash,
                    JWTTokenRecord.token_type == token_type,
                )
                .first()
            )
            row.revoked = revoked
            return True

    # Получение refresh токена по хешу
    def get_refresh_token_by_hash(self, token: str) -> JWTToken | None:
        """Получение refresh токена по хешу токена"""
        return self.get_token_by_hash(token, "refresh_token")

    # Обновление статуса revoked для refresh токена
    def update_refresh_token_revoked(self, token: str, revoked: bool = True) -> bool:
        """Обновление статуса revoked для refresh токена"""
        return self.update_token_revoked(token, "refresh_token", revoked)

    def update_token_revoked(self, token: str, token_type: TokenType, revoked: bool = True) -> bool:
        """Универсальный метод для обновления статуса revoked токена"""
        return self._update_token_revoked(token, token_type, revoked)

    # Создание access токена
    def create_access_token(self, user_id: int, token: str) -> JWTToken:
        """Создание access токена и сохранение в Redis/БД"""
        token_hash, created_at, expires_at = self._save_token(
            "access_token", user_id, token, settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        # Возвращаем объект JWTToken
        return JWTToken(
            user_id=user_id,
            token_type="access_token",
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=created_at,
            revoked=False,
        )

    # Получение access токена по хешу
    def get_access_token_by_hash(self, token: str) -> JWTToken | None:
        """Получение access токена по хешу токена"""
        return self.get_token_by_hash(token, "access_token")

    # Обновление статуса revoked для access токена
    def update_access_token_revoked(self, token: str, revoked: bool = True) -> bool:
        """Обновление статуса revoked для access токена"""
        return self.update_token_revoked(token, "access_token", revoked)


# Глобальный экземпляр репозитория
jwt_tokens_repository = JWTTokensRepository()
