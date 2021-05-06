from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.dependencies import PaginationQueryParams, authenticate_user, get_db
from app.models.user import User
from app.schemas.user import (
    UserCreateSchema,
    UserListSchema,
    UserSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/{user_id}', response_model=UserSchema, dependencies=[Depends(authenticate_user)]
)
def get_user(*, db: Session = Depends(get_db), user_id: int) -> Any:
    user = user_crud.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    return user


@router.post('', response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(*, db: Session = Depends(get_db), user_data: UserCreateSchema) -> Any:
    user = user_crud.get_by_login(db, user_data.login)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='User with such email already exist',
        )
    return user_crud.create(db, user_data)


@router.get(
    '', response_model=UserListSchema, dependencies=[Depends(authenticate_user)]
)
def get_users(
    *, db: Session = Depends(get_db), pagination: PaginationQueryParams = Depends()
) -> Any:
    return user_crud.get_multi(db, pagination.skip, pagination.limit)


@router.put(
    '/{user_id}', response_model=UserSchema, dependencies=[Depends(authenticate_user)]
)
def update_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(authenticate_user),
    user_id: int,
    user_data: UserUpdateSchema
) -> Any:
    user = user_crud.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    if user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Cannot update account of another user',
        )
    return user_crud.update(db, user, user_data)


@router.delete(
    '/{user_id}',
    response_model=UserSchema,
)
def delete_user(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(authenticate_user),
    user_id: int
) -> Any:
    user = user_crud.get(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )
    if user != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Cannot delete account of another user',
        )
    return user_crud.remove(db, user_id)
