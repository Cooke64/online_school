from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.course.router import router as course_router
from src.students.router import router as student_router
from starlette.requests import Request
from starlette.responses import Response

from src.database import SessionLocal


def incculde_routers(my_app):
    my_app.include_router(auth_router)
    my_app.include_router(course_router)
    my_app.include_router(student_router)


def get_application() -> FastAPI:
    application = FastAPI(
        title='myAppp',
        description='Проект',
        version='1.0.1'
    )

    # application.add_middleware(
    #     CORSMiddleware,
    #     allow_origins=['localhost'],
    #     allow_credentials=True,
    #     allow_methods=('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    #     allow_headers=['http://localhost:3000']
    # )
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