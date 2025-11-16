# Product Importer – FastAPI + Celery

A backend service to import ~500k products from CSV into PostgreSQL with:

- Async CSV import using Celery & Redis (handles long-running jobs)
- Product CRUD APIs with filtering & pagination
- Webhook management (add / edit / delete / test)
- Import job status API for real-time progress
- Simple HTML UI to upload CSV and manage products

This implementation is based on the Acme Inc. “Product Importer” assignment.

---

## 1. Tech Stack

- **Backend Framework**: FastAPI
- **Async Worker**: Celery
- **Broker / Result Backend**: Redis
- **Database**: PostgreSQL + SQLAlchemy ORM
- **API Docs**: Swagger UI (`/docs`) & ReDoc (`/redoc`)
- **Simple UI**: Plain HTML + JS (optional helper for testing)

---

## 2. Project Structure (backend)

```text
product_importer/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── celery_app.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── api/
│   │   ├── deps.py
│   │   └── routes/
│   │       ├── uploads.py      # CSV import
│   │       ├── products.py     # Product CRUD + bulk delete
│   │       ├── webhooks.py     # Webhook CRUD + test
│   │       └── health.py
│   ├── workers/
│   │   ├── import_worker.py
│   │   └── webhook_worker.py
│   └── celery_worker.py
├── ui/
│   └── index.html              # Simple UI to test APIs (optional)
├── requirements.txt
└── README.md
```

### 3. Prerequisites

Make sure you have:

Python 3.11+ (you’re using 3.12)

PostgreSQL running locally (or accessible DB URL)

Redis running on localhost:6379

pip / virtualenv (or python -m venv)


## 4. Setup – Clone & Install Dependencies

```
From your working directory:

# 1. Clone repo (or go into your existing folder)
git clone https://github.com/Prathik9/product_importer
cd product_importer

# 2. Create virtualenv
python3 -m venv venv

# 3. Activate virtualenv
source venv/bin/activate    # Linux / macOS
# .\venv\Scripts\activate   # Windows PowerShell

# 4. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

```

### 5. Configure Environment Variables

```
Create a .env file in the project root (product_importer/.env):

### Project
PROJECT_NAME="Product Importer"
API_PREFIX="/api"

### Database - adjust user/password/dbname/host/port for your setup

SQLALCHEMY_DATABASE_URI=postgresql+psycopg2://postgres:postgres@localhost:5432/product_importer

### Celery / Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1


Make sure the DB product_importer exists (or change the name in the URI).

```

### 6. Start Redis
If Redis is not running, start it.
On Ubuntu-like systems:

```
sudo service redis-server start
# or
redis-server


You should be able to connect at redis://localhost:6379/.
```

## 8. Run the FastAPI Application

From project root with venv active:
```
uvicorn app.main:app --reload --port 8000

```
You should see:

Uvicorn running on http://127.0.0.1:8000
Application startup complete.

API Documentation (Swagger)

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

You can view and test all APIs directly from Swagger UI (GET/POST/DELETE etc.).

## 9. Run Celery Worker

In another terminal (with same virtualenv activated):

```
cd /home/prathik/prathik_hp/pvp/LEARN/assesment/product_importer
source venv/bin/activate   # if not already

celery -A app.celery_worker.celery_app worker -l info -Q imports,webhooks

```
You should see something like:

```
[tasks]
  . app.workers.import_worker.import_products_task
  . app.workers.webhook_worker.send_webhook_task

celery@Dell-Latitude-3420 ready.

```
Now:

CSV uploads will enqueue an import task to imports queue.

Webhook test calls will enqueue to webhooks queue.

### 10 Run index.html from there you can see ui
```
Run 
index.html
```

## Swagger
```
Swagger: http://127.0.0.1:8000/docs
```
