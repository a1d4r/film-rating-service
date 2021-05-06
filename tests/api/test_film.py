from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from app.schemas.film import (
    FilmCreateSchema,
    FilmListSchema,
    FilmRatingSchema,
    FilmSchema,
    FilmUpdateSchema,
)
from tests.factories import FilmFactory, ReviewFactory


def test_get_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    film = FilmFactory()
    response = client.get(f'/films/{film.id}', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_film = FilmSchema.from_orm(film)
    retrieved_film = FilmSchema.parse_raw(response.text)
    assert actual_film == retrieved_film


def test_get_nonexistent_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    response = client.get('/films/1', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_films(client: TestClient, http_basic_auth: HTTPBasicAuth):
    films = FilmFactory.create_batch(3)
    response = client.get('/films', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_films = FilmListSchema(__root__=films)
    retrieved_films = FilmListSchema.parse_raw(response.text)
    assert actual_films == retrieved_films


def test_create_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    actual_film_data = FilmCreateSchema.from_orm(FilmFactory.build())
    response = client.post(
        '/films', json=jsonable_encoder(actual_film_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_201_CREATED

    print(response.text)
    retrieved_filmed_data = FilmCreateSchema.parse_raw(response.text)
    assert actual_film_data == retrieved_filmed_data


def test_update_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    film = FilmFactory()
    new_film_data = FilmUpdateSchema.from_orm(FilmFactory.build())
    response = client.put(
        f'/films/{film.id}', json=jsonable_encoder(new_film_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_film_data = FilmUpdateSchema.parse_raw(response.text)
    assert new_film_data == retrieved_film_data


def test_update_nonexistent_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    new_film_data = FilmUpdateSchema.from_orm(FilmFactory.build())
    response = client.put(
        '/films/1', json=jsonable_encoder(new_film_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    film = FilmFactory()
    response = client.delete(f'/films/{film.id}', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_film = FilmSchema.from_orm(film)
    retrieved_film = FilmSchema.parse_raw(response.text)
    assert actual_film == retrieved_film


def test_delete_nonexistent_film(client: TestClient, http_basic_auth: HTTPBasicAuth):
    response = client.delete('/films/1', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_film_rating(client: TestClient, http_basic_auth: HTTPBasicAuth):
    film = FilmFactory()
    ReviewFactory(film=film, rating=2, comment=None)
    ReviewFactory(film=film, rating=3, comment='')
    ReviewFactory(film=film, rating=10)
    response = client.get(f'/films/{film.id}/rating', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    expected_ratings = FilmRatingSchema(rating=5, num_ratings=3, num_reviews=1)
    actual_ratings = FilmRatingSchema.parse_raw(response.text)
    assert expected_ratings == actual_ratings


def test_get_nonexistent_film_rating(
    client: TestClient, http_basic_auth: HTTPBasicAuth
):
    response = client.put('/films/1/rating', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND
