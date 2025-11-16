from pydantic import BaseModel, AnyHttpUrl
from typing import Optional
from app.models.webhook import WebhookEvent


class WebhookBase(BaseModel):
    url: AnyHttpUrl
    event: WebhookEvent
    enabled: bool = True


class WebhookCreate(WebhookBase):
    pass


class WebhookUpdate(BaseModel):
    url: Optional[AnyHttpUrl] = None
    event: Optional[WebhookEvent] = None
    enabled: Optional[bool] = None


class WebhookOut(WebhookBase):
    id: int
    last_status_code: Optional[int]
    last_response_time_ms: Optional[int]
    last_error: Optional[str]

    class Config:
        model_config = {"from_attributes": True}

