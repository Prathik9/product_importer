from typing import Generator
from app.core.database import get_db


def get_db_dep() -> Generator:
    yield from get_db()
