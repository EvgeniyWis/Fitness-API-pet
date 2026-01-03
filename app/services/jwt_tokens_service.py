# Сервис для бизнес-логики JWT токенов
from app.repositories.jwt_tokens_repository import jwt_tokens_repository
from app.security.create_jwt_token import create_jwt_token
from app.core.config import settings
from datetime import datetime
from app.models.jwt_tokens import JWTToken, TokenType


class JWTTokensService:
    """Сервис для бизнес-логики JWT токенов"""
    
    def create_refresh_token(self, user_id: int, token: str) -> JWTToken:
        """Создание refresh токена"""
        return jwt_tokens_repository.create_refresh_token(user_id, token)

    def _check_token_exists(self, token: str, token_type: TokenType) -> bool:
        """Универсальная проверка наличия токена в БД"""
        jwt_token = jwt_tokens_repository.get_token_by_hash(token, token_type)
        return jwt_token is not None

    def _check_token_expired(self, token: str, token_type: TokenType) -> bool:
        """Универсальная проверка того не истёк ли токен и не инвалидирован ли он"""
        # Получаем сам токен из БД
        jwt_token: JWTToken | None = jwt_tokens_repository.get_token_by_hash(token, token_type)
        
        # Если токен не найден, то возвращаем True (считаем истекшим)
        if not jwt_token:
            return True

        # Проверяем не истёк ли токен
        is_expired = jwt_token.expires_at < datetime.now()
        
        # Если истёк, то инвалидируем токен
        if is_expired:
            self._invalidate_token(token, token_type)

        # Проверяем не инвалидирован ли токен
        is_revoked = jwt_token.revoked

        # Возвращаем True, если токен истёк или инвалидирован
        return is_expired or is_revoked

    def _invalidate_token(self, token: str, token_type: TokenType) -> bool:
        """Универсальная инвалидация токена"""
        return jwt_tokens_repository.update_token_revoked(token, token_type, revoked=True)

    def check_refresh_token_exists(self, token: str) -> bool:
        """Проверка наличия Refresh токена в БД"""
        return self._check_token_exists(token, "refresh_token")

    def check_refresh_token_expired(self, token: str) -> bool:
        """Проверка того не истёк ли Refresh токен и не инвалидирован ли он"""
        return self._check_token_expired(token, "refresh_token")

    def invalidate_refresh_token(self, token: str) -> bool:
        """Инвалидация Refresh токена"""
        return self._invalidate_token(token, "refresh_token")

    async def get_access_token_by_refresh_token(self, user_id: int, token: str) -> str | dict:
        """Получение Access токена по Refresh токену"""
        # Проверяем наличие Refresh токена в БД
        if not self.check_refresh_token_exists(token):
            return {"error": "Refresh токен не найден"}

        # Проверяем не истёк ли Refresh токен
        if self.check_refresh_token_expired(token):
            return {"error": "Refresh токен истёк"}

        # Генерируем Access токен
        access_token = create_jwt_token(user_id, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        # Сохраняем Access токен в Redis
        jwt_tokens_repository.create_access_token(user_id, access_token)
        
        return access_token

    def check_access_token_exists(self, token: str) -> bool:
        """Проверка наличия Access токена в БД"""
        return self._check_token_exists(token, "access_token")

    def check_access_token_expired(self, token: str) -> bool:
        """Проверка того не истёк ли Access токен и не инвалидирован ли он"""
        return self._check_token_expired(token, "access_token")

    def invalidate_access_token(self, token: str) -> bool:
        """Инвалидация Access токена"""
        return self._invalidate_token(token, "access_token")

# Глобальный экземпляр сервиса
jwt_tokens_service = JWTTokensService()
