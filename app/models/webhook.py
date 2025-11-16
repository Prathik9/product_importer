from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class WebhookEvent(str, enum.Enum):
    product_created = "product_created"
    product_updated = "product_updated"
    product_deleted = "product_deleted"
    import_completed = "import_completed"


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(512), nullable=False)
    event = Column(Enum(WebhookEvent), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)

    last_status_code = Column(Integer, nullable=True)
    last_response_time_ms = Column(Integer, nullable=True)
    last_error = Column(String(1024), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
