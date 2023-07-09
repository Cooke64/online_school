import os
import sys
from typing import Any
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from src.BaseModel import Base
from src.main_crud import get_db
from src.utils.create_router import create_router
from tests.utils.create_fake_bd import create_fake_bd
from tests.utils.users import auth_teachers, auth_students, UserHeaders

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def start_application():
    app = FastAPI()
    create_router(app)
    return app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    Base.metadata.create_all(engine)
    application = start_application()
    yield application
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(app: FastAPI) -> Generator:
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(
        app: FastAPI, db_session: SessionTesting
) -> Generator[TestClient, Any, None]:
    def get_test_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
def auth_teacher(client: TestClient, db_session: Session) -> UserHeaders:
    """Авторизация преподавателя"""
    return auth_teachers(client, session=db_session)


@pytest.fixture(scope="function")
def auth_student(client: TestClient, db_session: Session) -> UserHeaders:
    """Авторизация студента"""
    return auth_students(client, session=db_session)


@pytest.fixture(scope="function")
def get_fake_db(client: TestClient, db_session: Session) -> None:
    """Создание базы данных, в которой:
        - Пользователеь с ролью teacher
        - Три бесплатных курса без уроков
        - Один бесплатный курс с тремя уроками
        - Один платный курс с одинм уроком
        """
    return create_fake_bd(db_session)
