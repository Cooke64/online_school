from datetime import datetime

from sqlalchemy import Column as _, Integer, String, ForeignKey, \
    DateTime, Boolean
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.users.models import User


class StudentCourse(BaseModel):
    __tablename__ = "student_courses"
    student_id = _(Integer, ForeignKey('students.id'))
    course_id = _(Integer, ForeignKey('courses.id'))
    course_start = _(DateTime, nullable=False, default=datetime.utcnow)
    has_paid = _(Boolean, nullable=False, default=True)


class Student(BaseModel):
    __tablename__ = 'students'
    phone = _(String(50), unique=True, nullable=True)

    courses = relationship(
        'Course',
        secondary='student_courses',
        back_populates='students'
    )

    user_id = _(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=backref('student', uselist=False))
