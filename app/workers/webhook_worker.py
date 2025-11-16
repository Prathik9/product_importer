import time
import requests
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.webhook import Webhook
from app.schemas.product import ProductOut


@celery_app.task(name="app.workers.webhook_worker.send_webhook_task")
def send_webhook_task(webhook_id: int, payload: dict):
    db: Session = SessionLocal()
    try:
        webhook: Webhook | None = db.query(Webhook).get(webhook_id)
        if not webhook or not webhook.enabled:
            return

        start = time.time()
        try:
            res = requests.post(webhook.url, json=payload, timeout=5)
            elapsed_ms = int((time.time() - start) * 1000)

            webhook.last_status_code = res.status_code
            webhook.last_response_time_ms = elapsed_ms
            webhook.last_error = None
        except Exception as e:
            elapsed_ms = int((time.time() - start) * 1000)
            webhook.last_status_code = None
            webhook.last_response_time_ms = elapsed_ms
            webhook.last_error = str(e)

        db.add(webhook)
        db.commit()
    finally:
        db.close()
