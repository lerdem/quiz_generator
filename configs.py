import os


class Config:
    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql'
        f'://{os.environ["POSTGRES_USER"]}'
        f':{os.environ["POSTGRES_PASSWORD"]}'
        f'@{os.environ["POSTGRES_HOST"]}'
        f':{os.environ["POSTGRES_PORT"]}'
        f'/{os.environ["POSTGRES_DB"]}'
    )

    # redis config
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = (
        f"redis"
        f"://{os.environ['CACHE_REDIS_HOST']}"
        f":{os.environ['CACHE_REDIS_PORT']}"
        f"/{os.environ['CACHE_REDIS_DB']}"
    )
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_KEY_PREFIX = 'main'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
