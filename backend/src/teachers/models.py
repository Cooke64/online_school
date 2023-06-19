from sqlalchemy import Column as _, String, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from src.BaseModel import BaseModel
from src.users.models import User


class TeacherCourse(BaseModel):
    __tablename__ = "teacher_courses"
    user_id = _(Integer, ForeignKey('teachers.id'))
    course_id = _(Integer, ForeignKey('courses.id'))


class Teacher(BaseModel):
    __tablename__ = 'teachers'
    description = _(String, nullable=True)

    courses = relationship(
        'Course',
        secondary='teacher_courses',
        back_populates='teachers'
    )

    user_id = _(Integer, ForeignKey('users.id'))
    user = relationship(
        User,
        backref=backref('teacher', uselist=False),
    )