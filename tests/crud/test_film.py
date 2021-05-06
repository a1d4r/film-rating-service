from sqlalchemy.orm import Session

from app.crud.film import film_crud
from app.schemas.film import FilmCreateSchema, FilmUpdateSchema
from tests.factories import FilmFactory, ReviewFactory


def test_get_film(db: Session):
    actual_film = FilmFactory()
    retrieved_film = film_crud.get(db, actual_film.id)
    assert retrieved_film == actual_film


def test_get_films(db: Session):
    actual_films = FilmFactory.create_batch(3)
    retrieved_films = film_crud.get_multi(db)
    assert actual_films == retrieved_films


def test_create_film(db: Session):
    actual_film_data = FilmCreateSchema.from_orm(FilmFactory.build())
    film = film_crud.create(db, actual_film_data)
    retrieved_filmed_data = FilmCreateSchema.from_orm(film)
    assert actual_film_data == retrieved_filmed_data


def test_update_film(db: Session):
    film = FilmFactory()
    db.refresh(film)
    new_film_data = FilmUpdateSchema.from_orm(FilmFactory.build())
    updated_film = film_crud.update(db, film, new_film_data)
    retrieved_film_data = FilmUpdateSchema.from_orm(updated_film)
    assert new_film_data == retrieved_film_data


def test_delete_film(db: Session):
    film = FilmFactory()
    deleted_film = film_crud.remove(db, film.id)
    retrieved_film = film_crud.get(db, film.id)
    assert film == deleted_film
    assert retrieved_film is None


def test_get_film_rating():
    film = FilmFactory()
    ReviewFactory(film=film, rating=2)
    ReviewFactory(film=film, rating=3)
    ReviewFactory(film=film, rating=10)
    assert film.rating == 5
