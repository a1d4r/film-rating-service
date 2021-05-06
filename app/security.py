from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.user import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_user_password(db: Session, username: str, password: str) -> Optional[User]:
    from app.crud.user import user_crud  # noqa

    user = user_crud.get_by_login(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
