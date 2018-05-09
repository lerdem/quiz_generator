import os
from jinja2 import StrictUndefined


class Config:
    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
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
    REDIS_URL = (
        f"redis"
        f"://{os.environ['CACHE_REDIS_HOST']}"
        f":{os.environ['CACHE_REDIS_PORT']}/"
    )
    CACHE_REDIS_URL = REDIS_URL + os.environ['CACHE_REDIS_DB']
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_KEY_PREFIX = 'main'

    # celery
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_BROKER_URL = REDIS_URL + os.environ['CELERY_BROKER_DB']
    CELERY_RESULT_BACKEND = REDIS_URL + os.environ['CELERY_RESULT_DB']

    # celerybeat
    CELERY_IMPORTS = ('app.account.tasks', )
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
            'task': 'app.account.tasks.add_together',
            'schedule': 30.0,
            'args': (16, 16)
        },
    }

    JINJA_UNDEFINED = StrictUndefined

    COMPRESS_MIMETYPES = ('text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript')
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True


class ProdConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    LIVESERVER_PORT = 5001
