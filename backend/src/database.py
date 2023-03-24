from fastapi import Depends
from sqlalchemy import Column as _, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request

from src.config import settings

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = _(
        Integer(), nullable=False,
        unique=True, primary_key=True, autoincrement=True
    )


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db(request: Request):
    return request.state.db


class BaseCrud:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_current_item(self, id_item, Model):
        return self.session.query(Model).filter(Model.id == id_item).first()

    def create_item(self, item):
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def remove_item(self, id_item, Model):
        item = self.get_current_item(id_item, Model)
        self.session.delete(item)
        self.session.commit()
