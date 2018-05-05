import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_migrate import Migrate

from configs import Config
from views import Index

app = Flask(__name__)
app.config.from_object(f'configs.{os.environ["CONFIG_CLASS"]}')
db = SQLAlchemy(app)
cache = Cache(app)
migrate = Migrate(app, db)
celery = Config.make_celery(app)


@celery.task()
def add_together(a, b):
    return a + b

Index.get = cache.cached(timeout=3)(Index.get)  # check cache

app.add_url_rule('/', view_func=Index.as_view('index'))
