import app.factories as factories

app = factories.create_app()
celery = factories.create_celery(app)
