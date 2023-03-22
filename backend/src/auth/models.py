from sqlalchemy import Column as _, Integer, String, Boolean

from src.database import BaseModel


class User(BaseModel):
    __tablename__ = 'users'
    username = _(String, unique=True, nullable=False)
    email = _(String, unique=True, nullable=False)
    password = _(String, nullable=False)
    is_active = _(Boolean, default=False)
