import factory
from faker import Faker

from app.models.film import Film
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewCreateSchema
from app.schemas.user import UserCreateSchema
from app.security import get_password_hash

fake = Faker()


class BaseModelFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        sqlalchemy_session_persistence = 'commit'


class FilmFactory(BaseModelFactory):
    class Meta:
        model = Film

    title = factory.Faker('sentence', nb_words=3)
    year = factory.Faker('year')


class UserFactory(BaseModelFactory):
    class Meta:
        model = User

    login = factory.Sequence(lambda n: f'user{n}')
    hashed_password = factory.Sequence(lambda n: get_password_hash(f'password{n}'))


class UserCreateFactory(factory.Factory):
    class Meta:
        model = UserCreateSchema

    login = factory.Sequence(lambda n: f'user_{n}')
    password = factory.Sequence(lambda n: f'password_{n}')


class ReviewFactory(BaseModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    film = factory.SubFactory(FilmFactory)
    rating = factory.Faker('pyint', min_value=0, max_value=10)
    comment = factory.Faker('paragraph')


class ReviewCreateFactory(factory.Factory):
    class Meta:
        model = ReviewCreateSchema

    film_id = factory.Sequence(lambda n: n)
    rating = factory.Faker('pyint', min_value=0, max_value=10)
    comment = factory.Faker('paragraph')


sqlalchemy_factories = [FilmFactory, UserFactory, ReviewFactory]
