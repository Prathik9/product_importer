from app.core.celery_app import celery_app  # noqa: F401

# This file is just the entrypoint for Celery:
# celery -A app.celery_worker.celery_app worker -l info
# 🔥 force Celery to load task modules
import app.workers.import_worker
import app.workers.webhook_worker