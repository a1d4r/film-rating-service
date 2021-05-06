from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.review import review_crud
from app.dependencies import PaginationQueryParams, authenticate_user, get_db
from app.models.user import User
from app.schemas.review import (
    ReviewCreateSchema,
    ReviewListSchema,
    ReviewSchema,
    ReviewUpdateSchema,
)

router = APIRouter(
    prefix='/reviews', tags=['reviews'], dependencies=[Depends(authenticate_user)]
)


@router.get('/{review_id}', response_model=ReviewSchema)
def get_review(*, db: Session = Depends(get_db), review_id: int) -> Any:
    review = review_crud.get(db, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Review not found'
        )
    return review


@router.post('', response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
def create_review(
    *,
    db: Session = Depends(get_db),
    user: User = Depends(authenticate_user),
    review_data: ReviewCreateSchema
) -> Any:
    return review_crud.create_with_user(db, user, review_data)


@router.get('', response_model=ReviewListSchema)
def get_reviews(
    *, db: Session = Depends(get_db), pagination: PaginationQueryParams = Depends()
) -> Any:
    return review_crud.get_multi(db, skip=pagination.skip, limit=pagination.limit)


@router.put('/{review_id}', response_model=ReviewSchema)
def update_review(
    *, db: Session = Depends(get_db), review_id: int, review_data: ReviewUpdateSchema
) -> Any:
    review = review_crud.get(db, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Review not found'
        )
    return review_crud.update(db, review, review_data)


@router.delete('/{review_id}', response_model=ReviewSchema)
def delete_review(*, db: Session = Depends(get_db), review_id: int) -> Any:
    review = review_crud.get(db, review_id)
    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Review not found'
        )
    return review_crud.remove(db, review_id)
