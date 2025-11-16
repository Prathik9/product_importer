from celery import Celery
from .config import get_settings

settings = get_settings()

celery_app = Celery(
    "product_importer",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_routes={
        "app.workers.import_worker.*": {"queue": "imports"},
        "app.workers.webhook_worker.*": {"queue": "webhooks"},
    },
)
celery_app.autodiscover_tasks(['app.workers'])

