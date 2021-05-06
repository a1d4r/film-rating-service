from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.film import Film
from app.schemas.film import FilmCreateSchema, FilmUpdateSchema

from .base import CRUDBase


class CRUDFilm(CRUDBase[Film, FilmCreateSchema, FilmUpdateSchema]):
    def get_multi_with_filters(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        contains: Optional[str] = None,
        year: Optional[int] = None,
        sort_by_rating: Optional[bool] = False,
    ) -> List[Film]:
        films = db.query(Film)
        if contains:
            films = films.filter(Film.title.contains(contains))
        if year:
            films = films.filter(Film.year == year)
        if sort_by_rating:
            films = films.order_by(Film.rating.desc())
        films = films.offset(skip).limit(limit)
        return films.all()


film_crud = CRUDFilm(Film)
