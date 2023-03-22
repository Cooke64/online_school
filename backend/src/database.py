from datetime import datetime

from fastapi import Depends
from sqlalchemy import Column as _, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import sessionmaker
from starlette.requests import  Request

from src.config import settings

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = _(
        Integer(), nullable=False,
        unique=True, primary_key=True, autoincrement=True
    )
    created_at = _(DateTime, nullable=False, default=datetime.utcnow)


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db(request: Request):
    return request.state.db


class BaseCrud:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_item(self, item):
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
