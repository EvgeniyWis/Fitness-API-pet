from app.utils.db_decorator import with_db_session
from sqlalchemy.orm import Session
from app.core.config import settings
from app.security.token import hash_token
from datetime import datetime, timedelta
from typing import Optional


class JWTTokensRepository:
    """Репозиторий для работы с JWT токенами (только CRUD операции)"""

    # # Создание refresh токена
    # @with_db_session()
    # def create_refresh_token(self, db: Session, user_id: int, token: str) -> RefreshToken:
    #     """Создание refresh токена"""
    #     refresh_token = RefreshToken(
    #         user_id=user_id,
    #         expires_at=datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
    #         token_hash=hash_token(token)
    #     )
    #     db.add(refresh_token)
    #     db.commit()
    #     db.refresh(refresh_token)
    #     return refresh_token

    # # Получение refresh токена по хешу
    # @with_db_session()
    # def get_refresh_token_by_hash(self, db: Session, token: str) -> Optional[RefreshToken]:
    #     """Получение refresh токена по хешу токена"""
    #     return db.query(RefreshToken).filter(RefreshToken.token_hash == hash_token(token)).first()

    # # Обновление статуса revoked для refresh токена
    # @with_db_session()
    # def update_refresh_token_revoked(self, db: Session, token: str, revoked: bool = True) -> bool:
    #     """Обновление статуса revoked для refresh токена"""
    #     refresh_token = db.query(RefreshToken).filter(RefreshToken.token_hash == hash_token(token)).first()
        
    #     if not refresh_token:
    #         return False
            
    #     refresh_token.revoked = revoked
    #     db.commit()
    #     return True

# Глобальный экземпляр репозитория (в будущем будет заменен на работу с БД)
jwt_tokens_repository = JWTTokensRepository()

