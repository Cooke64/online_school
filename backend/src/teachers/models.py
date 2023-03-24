from sqlalchemy import Column as _, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.users.models import Role


class TeacherCourse(BaseModel):
    __tablename__ = "teacher_courses"
    user_id = _(Integer, ForeignKey('teachers.id'))
    project_id = _(Integer, ForeignKey('courses.id'))


class Teacher(BaseModel):
    __tablename__ = 'teachers'
    description = _(String, nullable=True)

    course = relationship('Course', secondary='teacher_courses',
                          back_populates='teacher'
                          )
    role = relationship(Role, backref=backref('teacher', uselist=False))
    role_id = _(Integer, ForeignKey('rols.id'))
