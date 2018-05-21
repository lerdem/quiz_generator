import os

from flask import Flask
from flask_assets import Bundle
from raven.contrib.celery import register_signal, register_logger_signal

from app import extensions as ext, error_handlers

CONFIG_MODULE = 'configs'


def create_celery(app, celery):

    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    app.extensions['celery'] = celery

    return celery


def create_app(conf_class=None):
    # create and configure application in runtime

    app = Flask('app.application')

    if conf_class is None:
        app.config.from_object(f'{CONFIG_MODULE}.{os.environ["CONFIG_CLASS"]}')
    else:
        app.config.from_object(f'{CONFIG_MODULE}.{conf_class}')

    app.jinja_env.undefined = app.config['JINJA_UNDEFINED']  # maybe there is a better way to pass this variable

    # init extensions
    ext.db.init_app(app)
    ext.cache.init_app(app)
    ext.migrate.init_app(app, ext.db)
    ext.compress.init_app(app)
    ext.assets.init_app(app)
    ext.sentry.init_app(app)
    ext.html_min.init_app(app)
    ext.login_manager.init_app(app)
    create_celery(app, ext.celery)

    # logging
    for handler in app.config['LOGGING_HANDLERS']:
        handler.setLevel(app.config['LOGGING_LEVEL'])
        app.logger.addHandler(handler)

    # send celery errors
    ext.client.set_dsn(app.config['SENTRY_CONFIG']['dsn'])
    register_logger_signal(ext.client)
    register_signal(ext.client)
    register_logger_signal(ext.client, loglevel=app.config['LOGGING_LEVEL'])

    # static slim
    js = Bundle(
        os.path.join('js', 'main.js'),
        filters='jsmin',
        output=os.path.join(app.config['COMPRESS_STATIC_DIR'], 'packed.js'),
    )
    css = Bundle(
        os.path.join('css', 'main.css'),
        filters='cssmin',
        output=os.path.join(app.config['COMPRESS_STATIC_DIR'], 'packed.css')
    )
    ext.assets.register('js_all', js)
    ext.assets.register('css_all', css)

    # urls
    from app.account.views import blueprint as account_bp

    app.register_blueprint(account_bp)

    # register error handlers
    app.register_error_handler(400, error_handlers.bad_request)
    app.register_error_handler(401, error_handlers.unauthorized)
    app.register_error_handler(403, error_handlers.forbidden)
    app.register_error_handler(404, error_handlers.not_found)
    app.register_error_handler(410, error_handlers.gone)
    app.register_error_handler(500, error_handlers.internal_server)

    # debug toolbar
    if app.config['DEBUG']:
        from flask_debugtoolbar import DebugToolbarExtension
        DebugToolbarExtension(app)

    return app
