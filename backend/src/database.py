from typing import Any

from fastapi import Depends
from sqlalchemy import Column as _, Integer, exists
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session, Query
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.config import settings
from src.exceptions import NotFound

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = _(
        Integer(), nullable=False,
        unique=True, primary_key=True, autoincrement=True
    )

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self)


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db(request: Request):
    return request.state.db


class BaseCrud:
    def __init__(self, session: Session = Depends(get_db)):
        self.session = session

    def get_user_by_email(self, Model, email):
        return self.session.query(Model).filter(Model.email == email).first()

    def get_all_items(self, Model) -> list:
        return self.session.query(Model).all()

    def get_current_item(self, id_item: int, Model: Any) -> Query:
        """Возвращает Объект построения SQL на уровне ORM.
        :param id_item: первичный ключ
        :type id_item: int
        :param Model: класс модели базы данных
        :type Model: Any
        :rtype: Query
        :return: ORM-level SQL construction object.
        """
        query = self.session.query(Model).filter(Model.id == id_item)
        if not query.first():
            raise NotFound
        return query

    def create_item(self, item):
        """
        Создает объект и возвращает его объект.
        :param item: любой объект модели, который может быть добавлен в бд
        """
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def remove_item(self, id_item: int, Model):
        item = self.get_current_item(id_item, Model).first()
        if not item:
            raise NotFound
        self.session.delete(item)
        self.session.commit()

    def check_item_exists(self, id_item: int, Model: Any) -> bool:
        is_exists = self.session.query(
            exists().where(Model.id == id_item)).scalar()
        return is_exists

    def update_item(self, item_id, Model, data_to_update):
        item = self.get_current_item(item_id, Model).first()
        for var, value in vars(data_to_update).items():
            setattr(item, var, value) if value else None
        self.create_item(item)
        return item

    @staticmethod
    def get_json_reposnse(message, status_code):
        return JSONResponse(status_code=status_code, content={"message": message})