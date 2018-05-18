import pytest

from app.factories import create_app, create_celery
from app import extensions as ext


@pytest.fixture(scope='module')
def app():
    app = create_app("TestingConfig")
    create_celery(app, ext.celery)

    with app.app_context():
        ext.db.drop_all()
        ext.db.create_all()
        ext.assets._named_bundles = {}  # Clear the bundle list

    return app
