from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_dep
from app.services.import_service import create_import_job
from app.schemas.import_job import ImportJobOut
from app.models.import_job import ImportJob
from app.core.database import SessionLocal
from app.core.celery_app import celery_app

router = APIRouter(prefix="/imports", tags=["imports"])


@router.post("/upload", response_model=ImportJobOut)
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db_dep),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")

    content_bytes = await file.read()
    content_str = content_bytes.decode("utf-8", errors="ignore")

    job = create_import_job(db, filename=file.filename)

    celery_app.send_task(
        "app.workers.import_worker.import_products_task",
        args=[job.id, content_str],
    )

    return job


@router.get("/{job_id}", response_model=ImportJobOut)
def get_import_status(job_id: int, db: Session = Depends(get_db_dep)):
    job: ImportJob | None = db.query(ImportJob).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
