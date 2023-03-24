from datetime import datetime

from sqlalchemy import Column as _, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from src.users.models import  Role
from src.course.models import Course
from src.database import Base, BaseModel

StudentCourse = Table('student_courses',
                      Base.metadata,
                      _('student_id', Integer, ForeignKey('students.id')),
                      _('course_id', Integer, ForeignKey('courses.id')),
                      _('course_start', DateTime, nullable=False,
                        default=datetime.utcnow)
                      )


class Student(BaseModel):
    __tablename__ = 'students'
    phone = _(String(50), unique=True, nullable=False)
    student_course = relationship(
        'Student', secondary=Course,
        primaryjoin=(StudentCourse.c.student_id == id),
        secondaryjoin=(StudentCourse.c.course_id == id),
        backref='student',
        lazy='dynamic'
    )
    role = relationship(Role, backref=backref('student', uselist=False))
