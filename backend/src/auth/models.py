
from sqlalchemy import Column as _, UUID, Integer, ForeignKey
from uuid import uuid4
from src.database import BaseModel


class Verification(BaseModel):
    __tablename__ = 'auth_verification'
    link = _(UUID(as_uuid=True), default=uuid4)
    user_id = _(Integer, ForeignKey('students.id'))
