from sqlalchemy import Column as _, String
from sqlalchemy.orm import relationship

from src.auth.models import User


class Teacher(User):
    __tablename__ = 'teachers'
    description = _(String, nullable=True)
    course = relationship('Course', back_populates='teacher')
