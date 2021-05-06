from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
from sqlalchemy.orm import Session

from app.crud.user import user_crud
from app.schemas.review import (
    ReviewCreateSchema,
    ReviewListSchema,
    ReviewSchema,
    ReviewUpdateSchema,
)
from tests.factories import FilmFactory, ReviewCreateFactory, ReviewFactory


def test_get_review(client: TestClient, http_basic_auth: HTTPBasicAuth):
    review = ReviewFactory()
    response = client.get(f'/reviews/{review.id}', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_review = ReviewSchema.from_orm(review)
    retrieved_review = ReviewSchema.parse_raw(response.text)
    assert actual_review == retrieved_review


def test_get_nonexistent_review(client: TestClient, http_basic_auth: HTTPBasicAuth):
    response = client.get('/reviews/1', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_reviews(client: TestClient, http_basic_auth: HTTPBasicAuth):
    reviews = ReviewFactory.create_batch(3)
    response = client.get('/reviews', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_reviews = ReviewListSchema(__root__=reviews)
    retrieved_reviews = ReviewListSchema.parse_raw(response.text)
    assert actual_reviews == retrieved_reviews


def test_create_review(db: Session, client: TestClient, http_basic_auth: HTTPBasicAuth):
    user = user_crud.get_multi(db)[0]  # there is already one from basic auth
    film = FilmFactory()
    actual_review_data = ReviewCreateFactory(user_id=user.id, film_id=film.id)
    response = client.post(
        '/reviews', json=jsonable_encoder(actual_review_data), auth=http_basic_auth
    )
    assert response.status_code == status.HTTP_201_CREATED

    retrieved_reviewed_data = ReviewCreateSchema.parse_raw(response.text)
    assert actual_review_data == retrieved_reviewed_data


def test_update_review(client: TestClient, http_basic_auth: HTTPBasicAuth):
    review = ReviewFactory()
    new_review_data = ReviewUpdateSchema.from_orm(ReviewCreateFactory())
    response = client.put(
        f'/reviews/{review.id}',
        json=jsonable_encoder(new_review_data),
        auth=http_basic_auth,
    )
    assert response.status_code == status.HTTP_200_OK

    retrieved_review_data = ReviewUpdateSchema.parse_raw(response.text)
    assert new_review_data == retrieved_review_data


def test_update_nonexistent_review(client: TestClient, http_basic_auth: HTTPBasicAuth):
    new_review_data = ReviewUpdateSchema.from_orm(ReviewCreateFactory())
    response = client.put(
        '/reviews/1',
        json=jsonable_encoder(new_review_data),
        auth=http_basic_auth,
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_review(client: TestClient, http_basic_auth: HTTPBasicAuth):
    review = ReviewFactory()
    response = client.delete(f'/reviews/{review.id}', auth=http_basic_auth)
    assert response.status_code == status.HTTP_200_OK

    actual_review = ReviewSchema.from_orm(review)
    retrieved_review = ReviewSchema.parse_raw(response.text)
    assert actual_review == retrieved_review


def test_delete_nonexistent_review(client: TestClient, http_basic_auth: HTTPBasicAuth):
    response = client.delete('/reviews/1', auth=http_basic_auth)
    assert response.status_code == status.HTTP_404_NOT_FOUND
