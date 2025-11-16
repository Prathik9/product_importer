from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.api.routes import products, uploads, webhooks, health
from app.core.database import Base, engine

settings = get_settings()

# create tables (for quick start; in prod prefer Alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# --- CORS should be here ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],             # allow everything for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Add routes AFTER CORS ---
app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(uploads.router, prefix=settings.API_PREFIX)
app.include_router(products.router, prefix=settings.API_PREFIX)
app.include_router(webhooks.router, prefix=settings.API_PREFIX)

