from sqlalchemy import Column as _, String
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.users.models import Role


class Teacher(BaseModel):
    __tablename__ = 'teachers'
    description = _(String, nullable=True)
    course = relationship('Course', back_populates='teacher')
    role = relationship(Role, backref=backref('teacher', uselist=False))
