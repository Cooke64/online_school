from datetime import datetime

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

    reviews = relationship(
        'CourseReview',
        back_populates='course'
    )
    course_preview = relationship('CoursePreviewImage', back_populates='course', uselist=False)


class CoursePreviewImage(BaseModel):
    __tablename__ = 'course_preview_photos'
    photo_blob = sa.Column(sa.LargeBinary, nullable=False)
    photo_type = sa.Column(sa.String, nullable=True)
    course_id = sa.Column(
        sa.Integer, sa.ForeignKey('courses.id'))
    course = relationship('Course', back_populates='course_preview')


class CourseReview(BaseModel):
    __tablename__ = 'courses_review'
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id'),
    )
    student_id = sa.Column(sa.Integer, sa.ForeignKey('students.id'))
    course_id = sa.Column(sa.Integer, sa.ForeignKey('courses.id'))
    text = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False,
                           default=datetime.utcnow)
    course = relationship('Course', back_populates='reviews')
    student = relationship('Student', back_populates='course_review')


class CourseRating(BaseModel):
    __tablename__ = 'courses_rating'
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

    student_pass = relationship(
        'Student',
        secondary='student_passed_lessons',
        back_populates='pass_lesson'
    )
    videos = relationship('LessonVideo', back_populates='lesson_content')
    photos = relationship('LessonPhoto', back_populates='lesson_content')

    comment = relationship(
        'LessonComment',
        back_populates='lesson'
    )
