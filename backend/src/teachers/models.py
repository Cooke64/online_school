from sqlalchemy import Column as _, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.users.models import Role


class Teacher(BaseModel):
    __tablename__ = 'teachers'
    description = _(String, nullable=True)
    course_id = _(Integer, ForeignKey('teachers.id'))
    course = relationship('Course', backref='teacher_for_course')

    role = relationship(Role, backref=backref('teacher', uselist=False))
    role_id = _(Integer, ForeignKey('rols.id'))
