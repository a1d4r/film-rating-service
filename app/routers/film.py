from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud.film import film_crud
from app.dependencies import PaginationQueryParams, authenticate_user, get_db
from app.schemas.film import (
    FilmCreateSchema,
    FilmListSchema,
    FilmRatingSchema,
    FilmSchema,
    FilmUpdateSchema,
)

router = APIRouter(
    prefix='/films', tags=['films'], dependencies=[Depends(authenticate_user)]
)


@router.get('/{film_id}', response_model=FilmSchema)
def get_film(*, db: Session = Depends(get_db), film_id: int) -> Any:
    film = film_crud.get(db, film_id)
    if film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Film not found'
        )
    return film


@router.post('', response_model=FilmSchema, status_code=status.HTTP_201_CREATED)
def create_film(*, db: Session = Depends(get_db), film_data: FilmCreateSchema) -> Any:
    return film_crud.create(db, film_data)


@router.get('', response_model=FilmListSchema)
def get_films(
    *,
    db: Session = Depends(get_db),
    pagination: PaginationQueryParams = Depends(),
    contains: Optional[str] = None,
    year: Optional[int] = None,
    sort_by_rating: Optional[bool] = False
) -> Any:
    return film_crud.get_multi_with_filters(
        db, pagination.skip, pagination.limit, contains, year, sort_by_rating
    )


@router.put('/{film_id}', response_model=FilmSchema)
def update_film(
    *, db: Session = Depends(get_db), film_id: int, film_data: FilmUpdateSchema
) -> Any:
    film = film_crud.get(db, film_id)
    if film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Film not found'
        )
    return film_crud.update(db, film, film_data)


@router.delete('/{film_id}', response_model=FilmSchema)
def delete_film(*, db: Session = Depends(get_db), film_id: int) -> Any:
    film = film_crud.get(db, film_id)
    if film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Film not found'
        )
    return film_crud.remove(db, film_id)


@router.get('/{film_id}/rating', response_model=FilmRatingSchema)
def get_average_rating_for_film(*, db: Session = Depends(get_db), film_id: int) -> Any:
    film = film_crud.get(db, film_id)
    if film is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Film not found'
        )
    return FilmRatingSchema(
        rating=film.rating,
        num_ratings=film.num_ratings,
        num_reviews=film.num_reviews,
    )
