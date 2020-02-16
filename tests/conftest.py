import pytest

from endymion import Endymion


@pytest.fixture
def app():
    return Endymion()


@pytest.fixture
def client(app):
    return app.test_session()
