import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.orm import declarative_base, sessionmaker

# Prefer root .env, fallback to api/.env
root_env = Path(__file__).resolve().parents[1] / ".env"
if root_env.exists():
    load_dotenv(root_env)
else:
    load_dotenv(Path(__file__).with_name(".env"))

DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("POSTGRESQL_DB")

if not DATABASE_URL:
    storage_dir = Path(__file__).resolve().parents[1] / "storage"
    storage_dir.mkdir(parents=True, exist_ok=True)
    db_file = storage_dir / "auto_backup.db"
    DATABASE_URL = f"sqlite:///{db_file.as_posix()}"

is_sqlite = DATABASE_URL.startswith("sqlite")

if is_sqlite:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    @event.listens_for(engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables and seed mock data if needed."""
    from api import models
    from api.mock_data import seed_mock_data

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        mock_mode = os.getenv("MOCK_MODE", "true").strip().lower() in ("true", "1", "yes")
        if mock_mode or is_sqlite:
            seed_mock_data(db)
    finally:
        db.close()
