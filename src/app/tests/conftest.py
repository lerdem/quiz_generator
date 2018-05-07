import pytest

from configs import Config


@pytest.fixture
def app():
    return Config.create_app('TestingConfig')
