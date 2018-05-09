import requests
from flask_testing import LiveServerTestCase

from app.factories import create_app, create_celery
from app.extensions import db, assets, celery


class BaseLiveServerTestCase(LiveServerTestCase):
    def create_app(self):
        app = create_app("TestingConfig")
        self.celery = create_celery(app, celery)

        with app.app_context():
            db.drop_all()
            db.create_all()

            assets._named_bundles = {}  # Clear the bundle list

        return app


class MyTest(BaseLiveServerTestCase):
    def test_flask_application_is_up_and_running(self):
        response = requests.get(self.get_server_url() + '/account/')
        self.assertEqual(response.status_code, 200)
