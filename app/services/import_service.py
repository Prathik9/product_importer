from sqlalchemy.orm import Session
from app.models.import_job import ImportJob, ImportStatus


def create_import_job(db: Session, filename: str) -> ImportJob:
    job = ImportJob(filename=filename, status=ImportStatus.pending)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def update_import_job(
    db: Session,
    job_id: int,
    *,
    status: ImportStatus | None = None,
    total_rows: int | None = None,
    processed_rows: int | None = None,
    error_message: str | None = None,
) -> ImportJob:
    job = db.query(ImportJob).get(job_id)
    if not job:
        raise ValueError("Import job not found")

    if status:
        job.status = status
    if total_rows is not None:
        job.total_rows = total_rows
    if processed_rows is not None:
        job.processed_rows = processed_rows
    if error_message is not None:
        job.error_message = error_message

    db.add(job)
    db.commit()
    db.refresh(job)
    return job
