
from sqlalchemy import Column as _, UUID, Integer, ForeignKey
from uuid import uuid4

from sqlalchemy.orm import relationship

from src.database import BaseModel


class Verification(BaseModel):
    __tablename__ = 'verifications'
    link = _(UUID(as_uuid=True), default=uuid4, unique=True, nullable=False)
    user_to_verify_id = _(Integer, ForeignKey('users.id'))
    user_to_verify = relationship('User', back_populates='verify_code')
