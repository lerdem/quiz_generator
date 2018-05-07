import os
from celery import Celery
from flask import Flask
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
    CACHE_REDIS_URL = (
        f"redis"
        f"://{os.environ['CACHE_REDIS_HOST']}"
        f":{os.environ['CACHE_REDIS_PORT']}"
        f"/{os.environ['CACHE_REDIS_DB']}"
    )
    CACHE_DEFAULT_TIMEOUT = 60
    CACHE_KEY_PREFIX = 'main'

    # celery
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_BROKER_URL = CELERY_RESULT_BACKEND = (
        f"redis"
        f"://{os.environ['CACHE_REDIS_HOST']}"
        f":{os.environ['CACHE_REDIS_PORT']}"
    )

    # celerybeat
    CELERYBEAT_SCHEDULE = {
        'add-every-30-seconds': {
            'task': 'app.account.tasks.add_together',
            'schedule': 30.0,
            'args': (16, 16)
        },
    }

    JINJA_UNDEFINED = StrictUndefined

    @classmethod
    def make_celery(cls, app):
        celery = Celery(
            app.import_name,
            backend=cls.CELERY_RESULT_BACKEND,
            broker=cls.CELERY_BROKER_URL,
        )
        celery.conf.update(app.config)

        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask
        return celery

    @classmethod
    def create_app(cls, conf_class=None):
        app = Flask(__name__)
        if conf_class is None:
            app.config.from_object(f'configs.{os.environ["CONFIG_CLASS"]}')
        else:
            app.config.from_object(f'configs.{conf_class}')
        return app


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProdConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SERVER_NAME = 'localhost:5001'
