from sqlalchemy import Column, Integer, String, DateTime, Enum, BigInteger
from sqlalchemy.sql import func
from app.core.database import Base
import enum


class ImportStatus(str, enum.Enum):
    pending = "pending"
    parsing = "parsing"
    validating = "validating"
    importing = "importing"
    completed = "completed"
    failed = "failed"


class ImportJob(Base):
    __tablename__ = "import_jobs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    status = Column(Enum(ImportStatus), default=ImportStatus.pending, nullable=False)
    total_rows = Column(BigInteger, nullable=True)
    processed_rows = Column(BigInteger, nullable=True, default=0)
    error_message = Column(String(1024), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
