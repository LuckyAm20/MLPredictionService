from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager
from .config import get_settings

settings = get_settings()

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)


def get_session():
    db = Session(engine)
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def init_db():
    SQLModel.metadata.create_all(engine)
