from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from const import (
    DB_ENGINE, DB_NAME, POSTGRES_USER,
    POSTGRES_PASSWORD, DB_HOST, DB_PORT
)


SQLALCHEMY_DATABASE_URL = (
        f"{DB_ENGINE}+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        + f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

DATABASE_URL = SQLALCHEMY_DATABASE_URL
DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Session:
    """
    Returns a database session.

    Returns:
        A generator that yields a database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
