from app.extensions import celery


@celery.task(bind=True)
def add_together(self, a, b):
    return a + b
