import pytest

from endymion import Endymion


@pytest.fixture
def app():
    return Endymion()
