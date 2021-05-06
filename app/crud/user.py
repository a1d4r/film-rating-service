from typing import Optional

from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreateSchema, UserUpdateSchema
from app.security import get_password_hash

from .base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreateSchema, UserUpdateSchema]):
    def get_by_login(self, db: Session, login: str) -> Optional[User]:
        return db.query(User).filter(User.login == login).first()

    def create(self, db: Session, obj_in: UserCreateSchema) -> User:
        hashed_password = get_password_hash(obj_in.password.get_secret_value())
        user = User(login=obj_in.login, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, db_obj: User, obj_in: UserUpdateSchema) -> User:
        if obj_in.password:
            db_obj.hashed_password = get_password_hash(
                obj_in.password.get_secret_value()
            )
        if obj_in.login:
            db_obj.login = obj_in.login
        db.add(db_obj)
        db.commit()
        return db_obj

    def remove(self, db: Session, id: int) -> Optional[User]:
        user = db.query(User).get(id)
        db.delete(user)
        db.commit()
        return user


user_crud = CRUDUser(User)
