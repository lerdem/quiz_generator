import app.factories as factories

app = factories.create_app()
celery = app.extensions['celery']
