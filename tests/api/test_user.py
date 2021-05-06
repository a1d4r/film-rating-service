from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.schemas.user import UserListSchema, UserSchema, UserUpdateSchema
from tests.factories import UserCreateFactory, UserFactory


def test_get_user(client: TestClient, http_basic_auth: HTTPBasicAuth):
    user = UserFactory()
    response = client.get(f'/users/{user.id}', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_user = UserSchema.from_orm(user)
    retrieved_user = UserSchema.parse_raw(response.text)
    assert actual_user == retrieved_user


def test_get_nonexistent_user(client: TestClient, http_basic_auth: HTTPBasicAuth):
    response = client.get('/users/10', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_users(db: Session, client: TestClient, http_basic_auth: HTTPBasicAuth):
    existing_users = user_crud.get_multi(db)
    users = UserFactory.create_batch(3)
    response = client.get('/users', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_users = UserListSchema(__root__=existing_users + users)
    retrieved_users = UserListSchema.parse_raw(response.text)
    assert actual_users == retrieved_users


def test_create_user(client: TestClient, http_basic_auth: HTTPBasicAuth):
    actual_user_data = UserCreateFactory()
    response = client.post(
        '/users', json=jsonable_encoder(actual_user_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_201_CREATED

    retrieved_user_data = UserSchema.parse_raw(response.text)
    assert actual_user_data.login == retrieved_user_data.login


def test_update_user(db: Session, client: TestClient, http_basic_auth: HTTPBasicAuth):
    user = user_crud.get_multi(db)[0]  # there is already one from basic auth
    new_user_data = UserUpdateSchema(**UserCreateFactory().dict())
    response = client.put(
        f'/users/{user.id}', json=jsonable_encoder(new_user_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_user_data = UserSchema.parse_raw(response.text)
    assert new_user_data.login == retrieved_user_data.login


def test_update_nonexistent_user(client: TestClient, http_basic_auth: HTTPBasicAuth):
    new_user_data = UserUpdateSchema(**UserCreateFactory().dict())
    response = client.put(
        '/users/10', json=jsonable_encoder(new_user_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user(db: Session, client: TestClient, http_basic_auth: HTTPBasicAuth):
    user = user_crud.get_multi(db)[0]  # there is already one from basic auth
    response = client.delete(f'/users/{user.id}', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_user = UserSchema.from_orm(user)
    retrieved_user = UserSchema.parse_raw(response.text)
    assert actual_user == retrieved_user


def test_delete_nonexistent_user(client: TestClient, http_basic_auth: HTTPBasicAuth):
    response = client.delete('/users/10', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND
