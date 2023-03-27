import warnings

from fastapi import FastAPI
from sqlalchemy import exc as sa_exc
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request

from src.course.router import router as course_router
from src.database import SessionLocal
from src.lessons.router import router as lesson_router
from src.students.router import router as student_router
from src.users.router import router as user_router
from .config import settings


def incculde_routers(my_app):
    my_app.include_router(user_router)
    my_app.include_router(course_router)
    my_app.include_router(student_router)
    my_app.include_router(lesson_router)


def get_application() -> FastAPI:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        warnings.simplefilter('ignore', category=sa_exc.SAWarning)
        application = FastAPI(
            title='myAppp',
            description='Проект',
            version='1.0.1'
        )

        application.add_middleware(
            CORSMiddleware,
            allow_origins=settings.allowed_cors,
            allow_credentials=True,
            allow_methods=settings.allowed_methods,
            allow_headers=['*']
        )
        incculde_routers(application)

        return application


app = get_application()


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

#  uvicorn src.api:app --reload
