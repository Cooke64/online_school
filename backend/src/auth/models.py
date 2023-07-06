from uuid import uuid4

from sqlalchemy import Column as _, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from src.BaseModel import BaseModel


class Verification(BaseModel):
    __tablename__ = 'verifications'
    __table_args__ = (
        UniqueConstraint('id', 'user_to_verify_id'),
    )
    link = _(Text(34), default=lambda: str(uuid4()), unique=True,
             nullable=False)
    user_to_verify_id = _(Integer, ForeignKey('users.id'))
    user_to_verify = relationship('User', back_populates='verify_code')
