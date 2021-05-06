from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.security import verify_user_password
from tests.factories import UserCreateFactory


def test_authenticate_user(db: Session) -> None:
    actual_user_data = UserCreateFactory()
    user_crud.create(db, actual_user_data)
    assert verify_user_password(
        db, actual_user_data.login, actual_user_data.password.get_secret_value()
    )
    assert not verify_user_password(db, actual_user_data.login, 'wrong_password')
    assert not verify_user_password(db, 'not_exist', 'not_exist')
