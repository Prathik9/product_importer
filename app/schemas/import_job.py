from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.import_job import ImportStatus


class ImportJobOut(BaseModel):
    id: int
    filename: str
    status: ImportStatus
    total_rows: Optional[int]
    processed_rows: Optional[int]
    error_message: Optional[str]
    created_at: datetime

    class Config:
        model_config = {"from_attributes": True}
