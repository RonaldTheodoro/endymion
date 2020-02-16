import pytest

from endymion import Endymion


@pytest.fixture
def app():
    return Endymion(templates_dir='tests/resources/templates')


@pytest.fixture
def client(app):
    return app.test_session()
