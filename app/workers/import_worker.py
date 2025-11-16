# app/workers/import_worker.py
import csv
from io import StringIO
from sqlalchemy.orm import Session
from app.core.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.import_job import ImportStatus
from app.services.import_service import update_import_job
from app.services.product_service import create_product
from app.schemas.product import ProductCreate


@celery_app.task(name="app.workers.import_worker.import_products_task")
def import_products_task(job_id: int, file_content: str):
    db: Session = SessionLocal()
    try:
        update_import_job(db, job_id, status=ImportStatus.parsing)

        # Load CSV
        f = StringIO(file_content)
        reader = csv.DictReader(f)

        # Validate header
        required_cols = {"sku", "name", "description", "price"}
        csv_cols = set(reader.fieldnames or [])
        missing = required_cols - csv_cols
        if missing:
            raise ValueError(f"Missing columns: {', '.join(missing)}")

        rows = list(reader)

        # Validate rows
        if len(rows) == 0:
            raise ValueError("CSV contains no product rows.")

        update_import_job(db, job_id, status=ImportStatus.importing, total_rows=len(rows))

        processed = 0

        for row in rows:
            # Clean whitespace SKU
            sku = (row.get("sku") or "").strip()
            if not sku:
                raise ValueError("Found row with empty SKU. SKU is required.")

            # Clean and parse price
            price_raw = row.get("price")
            if price_raw:
                price_raw = price_raw.strip()
                try:
                    price = float(price_raw)
                except ValueError:
                    raise ValueError(f"Invalid price value '{price_raw}' for SKU '{sku}'.")
            else:
                price = None

            product_data = ProductCreate(
                sku=sku,
                name=row.get("name") or sku,
                description=row.get("description"),
                price=price,
                active=True,
            )

            create_product(db, product_data)
            processed += 1

            # Update every 1000 rows so DB & UI stay smooth
            if processed % 1000 == 0:
                update_import_job(db, job_id, processed_rows=processed)

        update_import_job(
            db,
            job_id,
            status=ImportStatus.completed,
            processed_rows=processed
        )

    except Exception as e:
        # Store clean error message in DB for UI
        update_import_job(
            db,
            job_id,
            status=ImportStatus.failed,
            error_message=str(e)
        )
        raise

    finally:
        db.close()
