import os
import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


APP_MYSQL_HOST = os.getenv("RS_MYSQL_HOST")
APP_MYSQL_PORT = int(os.getenv("RS_MYSQL_PORT", "3306"))
APP_MYSQL_USER = os.getenv("RS_MYSQL_USER")
APP_MYSQL_PASSWORD = os.getenv("RS_MYSQL_PASSWORD")
APP_MYSQL_DATABASE = os.getenv("RS_MYSQL_DATABASE")

DATABASE_URL = (
    f"mysql+pymysql://{APP_MYSQL_USER}:{APP_MYSQL_PASSWORD}"
    f"@{APP_MYSQL_HOST}:{APP_MYSQL_PORT}/{APP_MYSQL_DATABASE}"
)

MAX_RETRIES = int(os.getenv("DB_MAX_RETRIES", "30"))
RETRY_DELAY = float(os.getenv("DB_RETRY_DELAY", "2"))

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True,
)

Base = declarative_base()


def wait_for_db():
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))

            print(f"[DB] Connection OK (attempt {attempt})")
            return

        except Exception as exc:
            last_error = exc
            print(f"[DB] Waiting MySQL ({attempt}/{MAX_RETRIES}): {exc}")
            time.sleep(RETRY_DELAY)

    raise RuntimeError(
        f"Unable to connect to MySQL after {MAX_RETRIES} attempts: {last_error}"
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()