import os


class Config:
    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://'
        f'{os.environ["POSTGRES_USER"]}'
        f':{os.environ["POSTGRES_PASSWORD"]}'
        f'@{os.environ["POSTGRES_HOST"]}'
        f':{os.environ["POSTGRES_PORT"]}'
        f'/{os.environ["POSTGRES_DB"]}'
    )


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
