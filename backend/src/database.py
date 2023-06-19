import typing
from typing import Any

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy import exists
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm import sessionmaker
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.auth.utils.jwt_bearer import get_current_user
from src.config import settings
from src.exceptions import NotFound
from src.users.models import User

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db(request: Request):
    return request.state.db


class UserPermission(typing.NamedTuple):
    role: str
    user_email: str


class BaseCrud:
    def __init__(self, session: Session = Depends(get_db),
                 email: str = Depends(get_current_user)):
        self.session: Session = session
        self.__email: str | None = email

    @property
    def user(self):
        user = self.get_user(self.__email)
        if not user:
            raise NotFound
        if user and user.is_active:
            return user

    @property
    def email(self):
        return self.__email

    @property
    def is_student(self):
        if self.user:
            return self.user.role == 'Student'

    @property
    def is_teacher(self):
        if self.user:
            return self.user.role == 'Teacher'

    def get_user(self, email: str | None = None) -> User:
        if not email:
            email = self.__email
        return self.session.query(User).filter(User.email == email).first()

    def get_all_items(self, Model) -> list:
        return self.session.query(Model).all()

    def get_current_item(self, id_item: int, Model: Any) -> Query:
        """Возвращает Объект построения SQL на уровне ORM.
        :param id_item: первичный ключ
        :type id_item: int
        :param Model: класс модели базы данных
        :type Model: Any
        :rtype: Query
        :return: ORM-level SQL construction object. | raise NotFound
        """
        query = self.session.query(Model).filter(Model.id == id_item)
        if not query.first():
            raise NotFound
        return query

    def create_item(self, item: Any) -> Any:
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
        return JSONResponse(
            status_code=status_code,
            content={"message": message}
        )
