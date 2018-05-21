import os
import logging.handlers

from jinja2 import StrictUndefined

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
LOGS_DIR = os.path.join(BASE_DIR, 'logs')


class Config:
    ENV = os.environ["ENV"]
    DEBUG = False
    TESTING = False
    BASE_DIR = BASE_DIR
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']

    # sqlalchemy
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
    REDIS_URL = (
        f"redis"
        f"://{os.environ['CACHE_REDIS_HOST']}"
        f":{os.environ['CACHE_REDIS_PORT']}/"
    )

    # cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = REDIS_URL + os.environ['CACHE_REDIS_DB']
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_KEY_PREFIX = 'main'

    # celery
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_BROKER_URL = REDIS_URL + os.environ['CELERY_BROKER_DB']
    CELERY_RESULT_BACKEND = REDIS_URL + os.environ['CELERY_RESULT_DB']

    # celerybeat
    CELERY_IMPORTS = ('app.account.tasks',)
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
            'task': 'app.account.tasks.add_together',
            'schedule': 30.0,
            'args': (16, 16)
        },
    }

    # jinja
    JINJA_UNDEFINED = StrictUndefined

    # compress
    COMPRESS_MIMETYPES = ('text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript')
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

    # assets
    COMPRESS_STATIC_DIR = os.path.join(BASE_DIR, 'app', 'static', 'compressed_static')
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = False

    # logging handlers
    FILE_HANDLER = logging.handlers.RotatingFileHandler(
        os.path.join(LOGS_DIR, 'app_logs', 'app.log'),
        maxBytes=1024 * 1024,
        backupCount=10,
    )

    # logging
    LOGGING_LEVEL = logging.WARNING
    LOGGING_HANDLERS = (
        FILE_HANDLER,
    )

    # sentry
    SENTRY_CONFIG = {'dsn': os.environ.get('SENTRY_DSN', '')}
    SENTRY_USER_ATTRS = ('username', 'first_name', 'last_name', 'email')

    # html minify
    # TODO test it
    MINIFY_PAGE = True


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True
    ASSETS_DEBUG = True
    ASSETS_AUTO_BUILD = True
    DEBUG_TB_PROFILER_ENABLED = True
    DEBUG_TB_TEMPLATE_EDITOR_ENABLED = True
    LOGGING_LEVEL = logging.DEBUG


class ProdConfig(Config):
    SENTRY_CONFIG = {'dsn': os.environ['SENTRY_DSN']}


class TestingConfig(Config):
    HASH_ROUNDS = 1
    TESTING = True
    ASSETS_AUTO_BUILD = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    LIVESERVER_PORT = 5001
    SENTRY_CONFIG = {
        'ignore_exceptions': [Exception],
        'dsn': '',
    }
    LOGGING_HANDLERS = ()
