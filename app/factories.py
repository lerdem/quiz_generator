import os

from flask import Flask
from celery import Celery
from flask_assets import Bundle

from configs import Config


def create_celery(app):
    celery = Celery(
        'celery',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app(conf_class=None):
    app = Flask('app.application')
    if conf_class is None:
        app.config.from_object(f'configs.{os.environ["CONFIG_CLASS"]}')
    else:
        app.config.from_object(f'configs.{conf_class}')
    app.jinja_env.undefined = Config.JINJA_UNDEFINED  # maybe there is a better way to pass this variable

    from app.extensions import db, cache, migrate, compress, assets
    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)
    assets.init_app(app)

    js = Bundle('js/main.js', filters='jsmin', output='compressed_static/packed.js')
    css = Bundle('css/main.css', filters='cssmin', output='compressed_static/packed.css')

    assets.register('js_all', js)
    assets.register('css_all', css)

    from app.account.views import blueprint as account_bp

    app.register_blueprint(account_bp)

    return app
