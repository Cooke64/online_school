import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Course(BaseModel):
    __tablename__ = 'courses'
    title = sa.Column(sa.String(199), nullable=False)
    description = sa.Column(sa.Text, nullable=False)
    lessons = relationship('Lesson', back_populates='course')
    is_free = sa.Column(sa.Boolean, default=False)

    students = relationship(
        'Student',
        secondary='student_courses',
        back_populates='courses'
    )
    teachers = relationship(
        'Teacher',
        secondary='teacher_courses',
        back_populates='courses'
    )

    ratings = relationship(
        'Student',
        secondary='courses_rating',
        back_populates='courses_rating'
    )


class CourseRating(BaseModel):
    __tablename__ = "courses_rating"
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id'),
    )
    student_id = sa.Column(sa.Integer, sa.ForeignKey('students.id'))
    course_id = sa.Column(sa.Integer, sa.ForeignKey('courses.id'))
    rating = sa.Column(sa.Integer, nullable=False, default=5)


class Lesson(BaseModel):
    __tablename__ = 'lessons'
    title = sa.Column(sa.String(199), nullable=False)
    content = sa.Column(sa.Text, nullable=False)
    course_id = sa.Column(sa.Integer, sa.ForeignKey('courses.id'))
    course = relationship('Course', back_populates='lessons')
    is_trial = sa.Column(sa.Boolean, nullable=False, default=False)
