import logging
import warnings

from fastapi import FastAPI
from sqlalchemy import exc as sa_exc
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request


from .config import settings
from .database import SessionLocal
from .utils.create_router import create_router


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s'
)

logger = logging.getLogger(__name__)
logger.addHandler(logging.FileHandler('loger_data.log'))
logger.addHandler(logging.StreamHandler())


def get_application() -> FastAPI:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore")
        warnings.simplefilter('ignore', category=sa_exc.SAWarning)
        application: FastAPI = FastAPI(
            title='OnlineEducation School',
            description='Онлайн образовательный проект',
            version='1.2'
        )

        origins = ["*"]

        application.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        create_router(application)

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
