import pytest
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth

from app import main
from app.crud.user import user_crud
from app.database import Base
from app.dependencies import get_db
from tests.database import TestingSessionLocal, engine
from tests.factories import UserCreateFactory, sqlalchemy_factories


@pytest.fixture(autouse=True)
def init_db():
    from app.models import film, review, user  # noqa

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture()
def db():
    db = TestingSessionLocal()
    for factory in sqlalchemy_factories:
        # type: ignore
        factory._meta.sqlalchemy_session = db  # type: ignore # pylint: disable=W0212
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(db):
    main.app.dependency_overrides[get_db] = lambda: db
    with TestClient(main.app) as client:
        yield client


@pytest.fixture()
def http_basic_auth(db, init_db):  # pylint: disable=unused-argument
    user_data = UserCreateFactory()
    user_crud.create(db, user_data)
    return HTTPBasicAuth(user_data.login, user_data.password.get_secret_value())
