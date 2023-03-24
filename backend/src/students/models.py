from datetime import datetime

from sqlalchemy import Column as _, Integer, String, ForeignKey, \
    DateTime
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.users.models import Role


class StudentCourse(BaseModel):
    __tablename__ = "student_courses"
    student_id = _(Integer, ForeignKey('students.id'))
    course_id = _(Integer, ForeignKey('courses.id'))
    course_start = _(DateTime, nullable=False, default=datetime.utcnow)


class Student(BaseModel):
    __tablename__ = 'students'
    phone = _(String(50), unique=True, nullable=False)
    course = relationship(
        'Course', secondary='student_courses',
        backref='student',
    )
    role_id = _(Integer, ForeignKey('rols.id'))
    role = relationship(Role, backref=backref('student', uselist=False))

    def __repr__(self) -> str:
        return f'Staff(role_id={self.role_id!r},)'
