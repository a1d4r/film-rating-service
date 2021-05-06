from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.security import verify_password
from tests.factories import UserCreateFactory, UserFactory


def test_get_user(db: Session):
    actual_user = UserFactory()
    retrieved_user = user_crud.get(db, actual_user.id)
    assert actual_user == retrieved_user


def test_get_user_by_login(db: Session):
    actual_user = UserFactory()
    retrieved_user = user_crud.get_by_login(db, actual_user.login)
    assert actual_user == retrieved_user


def test_get_users(db: Session):
    actual_users = UserFactory.create_batch(3)
    retrieved_users = user_crud.get_multi(db)
    assert actual_users == retrieved_users


def test_create_user(db: Session):
    actual_user_data = UserCreateFactory()
    user = user_crud.create(db, actual_user_data)
    assert actual_user_data.login == user.login
    assert verify_password(
        actual_user_data.password.get_secret_value(), user.hashed_password
    )


def test_update_user(db: Session):
    user = UserFactory()
    new_user_data = UserCreateFactory()
    updated_user = user_crud.update(db, user, new_user_data)
    assert updated_user is not None
    assert new_user_data.login == updated_user.login
    assert verify_password(
        new_user_data.password.get_secret_value(), updated_user.hashed_password
    )


def test_delete_user(db: Session):
    user = UserFactory()
    deleted_user = user_crud.remove(db, user.id)
    retrieved_user = user_crud.get(db, user.id)
    assert user == deleted_user
    assert retrieved_user is None
