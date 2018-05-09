from celery import Celery
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_migrate import Migrate
from flask_compress import Compress
from flask_assets import Environment
from raven.contrib.flask import Sentry

from configs import Config


db = SQLAlchemy()
cache = Cache()
migrate = Migrate()
compress = Compress()
assets = Environment()
sentry = Sentry()
celery = Celery(
    'celery',
    backend=Config.CELERY_RESULT_BACKEND,
    broker=Config.CELERY_BROKER_URL,
)
