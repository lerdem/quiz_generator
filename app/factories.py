import os

from flask import Flask
from flask_assets import Bundle

from configs import Config


def create_celery(app, celery):

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    return celery


def create_app(conf_class=None):
    # create and configure application in runtime

    app = Flask('app.application')
    if conf_class is None:
        app.config.from_object(f'configs.{os.environ["CONFIG_CLASS"]}')
    else:
        app.config.from_object(f'configs.{conf_class}')
    app.jinja_env.undefined = Config.JINJA_UNDEFINED  # maybe there is a better way to pass this variable

    # init extensions
    from app.extensions import db, cache, migrate, compress, assets, sentry, celery

    db.init_app(app)
    cache.init_app(app)
    migrate.init_app(app, db)
    compress.init_app(app)
    assets.init_app(app)
    sentry.init_app(app)

    celery = create_celery(app, celery)

    app.extensions['celery'] = celery

    # static slim
    js = Bundle('js/main.js', filters='jsmin', output='compressed_static/packed.js')
    css = Bundle('css/main.css', filters='cssmin', output='compressed_static/packed.css')
    assets.register('js_all', js)
    assets.register('css_all', css)

    # TODO get handlers through app
    for handler in Config.LOGGING_HANDLERS:
        app.logger.addHandler(handler)

    # urls
    from app.account.views import blueprint as account_bp

    app.register_blueprint(account_bp)

    # register error handlers
    from app.error_handlers import (
        not_found, forbidden, bad_request,
        internal_server, unauthorized, gone,
    )
    app.register_error_handler(400, bad_request)
    app.register_error_handler(401, unauthorized)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, not_found)
    app.register_error_handler(410, gone)
    app.register_error_handler(500, internal_server)

    # debug toolbar
    if app.config['DEBUG']:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    return app
