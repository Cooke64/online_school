from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, event


class TimeStampMixin:
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    @staticmethod
    def _updated_at(mapper, connection, target) -> None:
        target.updated_at = datetime.utcnow()

    @classmethod
    def __declare_last__(cls) -> None:
        event.listen(cls, "before_update", cls._updated_at)


class ErrorMessage(BaseModel):
    message: str


class OrmBaseModel(BaseModel):
    class Config:
        orm_mode = True
        validate_assignment = True
