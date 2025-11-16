from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from app.api.deps import get_db_dep
from app.schemas.webhook import WebhookOut, WebhookCreate, WebhookUpdate
from app.models.webhook import Webhook
from app.core.celery_app import celery_app

router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@router.get("/", response_model=List[WebhookOut])
def list_webhooks(db: Session = Depends(get_db_dep)):
    return db.query(Webhook).all()


@router.post("/", response_model=WebhookOut)
def create_webhook(data: WebhookCreate, db: Session = Depends(get_db_dep)):
    webhook = Webhook(**data.dict())
    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


@router.put("/{webhook_id}", response_model=WebhookOut)
def update_webhook(
    webhook_id: int, data: WebhookUpdate, db: Session = Depends(get_db_dep)
):
    webhook = db.query(Webhook).get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    for field, value in data.dict(exclude_unset=True).items():
        setattr(webhook, field, value)

    db.add(webhook)
    db.commit()
    db.refresh(webhook)
    return webhook


@router.delete("/{webhook_id}")
def delete_webhook(webhook_id: int, db: Session = Depends(get_db_dep)):
    webhook = db.query(Webhook).get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    db.delete(webhook)
    db.commit()
    return {"detail": "Deleted"}


@router.post("/{webhook_id}/test", response_model=WebhookOut)
def test_webhook(webhook_id: int, db: Session = Depends(get_db_dep)):
    webhook = db.query(Webhook).get(webhook_id)
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")

    celery_app.send_task(
        "app.workers.webhook_worker.send_webhook_task",
        args=[webhook.id, {"test": True}],
    )

    # UI can refresh this webhook (GET /webhooks) to see last_status_code/time
    return webhook
