from datetime import datetime

from sqlalchemy import Column as _, Integer, String, Boolean, Table, \
    ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.course.models import Course
from src.database import BaseModel, Base


class User(BaseModel):
    __abstract__ = True
    first_name = _(String(50), unique=True, nullable=False)
    last_name = _(String(99), unique=True, nullable=True)
    username = _(String(50), unique=True, nullable=True)
    email = _(String(99), unique=True, nullable=False)
    password = _(String, nullable=False)
    is_active = _(Boolean, default=False)


class Teacher(User):
    __tablename__ = 'teachers'
    description = _(String, nullable=True)
    course = relationship('Course', back_populates='teacher')


StudentCourse = Table('student_courses',
                      Base.metadata,
                      _('student_id', Integer, ForeignKey('students.id')),
                      _('course_id', Integer, ForeignKey('courses.id')),
                      _('course_start', DateTime, nullable=False, default=datetime.utcnow)
                      )


class Student(User):
    __tablename__ = 'students'
    phone = _(String(50), unique=True, nullable=False)
    student_course = relationship(
        'Student', secondary=Course,
        primaryjoin=(StudentCourse.c.student_id == id),
        secondaryjoin=(StudentCourse.c.course_id == id),
        backref='student',
        lazy='dynamic'
    )
