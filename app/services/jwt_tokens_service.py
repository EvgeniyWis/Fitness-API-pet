# Сервис для бизнес-логики JWT токенов
from app.repositories.jwt_tokens_repository import jwt_tokens_repository
from app.security.create_jwt_token import create_jwt_token
from app.core.config import settings
from datetime import datetime


class JWTTokensService:
    """Сервис для бизнес-логики JWT токенов"""
    
    # def create_refresh_token(self, user_id: int, token: str) -> RefreshToken:
    #     """Создание refresh токена"""
    #     return jwt_tokens_repository.create_refresh_token(user_id, token)

    # def check_refresh_token_exists(self, token: str) -> bool:
    #     """Проверка наличия Refresh токена в БД"""
    #     refresh_token = jwt_tokens_repository.get_refresh_token_by_hash(token)
    #     return refresh_token is not None

    # def check_refresh_token_expired(self, token: str) -> bool:
    #     """Проверка того не истёк ли Refresh токен и не инвалидирован ли он"""
    #     # Получаем сам токен из БД
    #     refresh_token: RefreshToken | None = jwt_tokens_repository.get_refresh_token_by_hash(token)
        
    #     # Если токен не найден, то возвращаем True (считаем истекшим)
    #     if not refresh_token:
    #         return True

    #     # Проверяем не истёк ли Refresh токен
    #     is_expired = refresh_token.expires_at < datetime.now()
        
    #     # Если истёк, то инвалидируем Refresh токен
    #     if is_expired:
    #         self.invalidate_refresh_token(token)

    #     # Проверяем не инвалидирован ли Refresh токен
    #     is_revoked = refresh_token.revoked

    #     # Возвращаем True, если Refresh токен истёк или инвалидирован
    #     return is_expired or is_revoked

    # def invalidate_refresh_token(self, token: str) -> bool:
    #     """Инвалидация Refresh токена"""
    #     return jwt_tokens_repository.update_refresh_token_revoked(token, revoked=True)

    # async def get_access_token_by_refresh_token(self, user_id: int, token: str) -> str | dict:
    #     """Получение Access токена по Refresh токену"""
    #     # Проверяем наличие Refresh токена в БД
    #     if not self.check_refresh_token_exists(token):
    #         return {"error": "Refresh токен не найден"}

    #     # Проверяем не истёк ли Refresh токен
    #     if self.check_refresh_token_expired(token):
    #         return {"error": "Refresh токен истёк"}

    #     # Генерируем Access токен
    #     access_token = create_jwt_token(user_id, settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    #     return access_token

# Глобальный экземпляр сервиса
jwt_tokens_service = JWTTokensService()
