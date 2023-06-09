from datetime import datetime

from sqlalchemy import Column as _, Integer, String, ForeignKey, \
    DateTime, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from src.BaseModel import BaseModel
from src.students_awards.models import StudentAward
from src.users.models import User


class StudentCourse(BaseModel):
    __tablename__ = 'student_courses'
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id'),
    )
    student_id = _(Integer, ForeignKey('students.id'))
    course_id = _(Integer, ForeignKey('courses.id'))
    course_start = _(DateTime, nullable=False, default=datetime.utcnow)
    has_paid = _(Boolean, nullable=False, default=False)


class StudentPassedLesson(BaseModel):
    __tablename__ = 'student_passed_lessons'
    __table_args__ = (
        UniqueConstraint('student_id', 'lesson_id'),
    )
    student_id = _(Integer, ForeignKey('students.id'))
    lesson_id = _(Integer, ForeignKey('lessons.id'))
    has_pass = _(Boolean, nullable=False, default=False)
    when_pass = _(DateTime(timezone=True), nullable=True)


class FavoriteLesson(BaseModel):
    __tablename__ = 'favorite_lessons'
    __table_args__ = (
        UniqueConstraint('student_id', 'lesson_id'),
    )
    student_id = _(Integer, ForeignKey('students.id'))
    lesson_id = _(Integer, ForeignKey('lessons.id'))


class FavoriteCourse(BaseModel):
    __tablename__ = 'favorite_courses'
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id'),
    )
    student_id = _(Integer, ForeignKey('students.id'))
    course_id = _(Integer, ForeignKey('courses.id'))


class Student(BaseModel):
    __tablename__ = 'students'
    phone = _(String(50), unique=True, nullable=True)

    courses = relationship(
        'Course',
        secondary='student_courses',
        back_populates='students'
    )

    favorite_courses = relationship(
        'Course',
        secondary='favorite_courses',
        back_populates='favorite_student_course'
    )

    user_id = _(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=backref('student', uselist=False))

    courses_rating = relationship(
        'Course',
        secondary='courses_rating',
        back_populates='ratings'
    )

    pass_lesson = relationship(
        'Lesson',
        secondary='student_passed_lessons',
        back_populates='student_pass'
    )

    favorite_lessons = relationship(
        'Lesson',
        secondary='favorite_lessons',
        back_populates='favorite_student_lessons'
    )

    course_review = relationship(
        'CourseReview',
        back_populates='student'
    )

    lesson_comment = relationship(
        'LessonComment',
        back_populates='student'
    )

    student_award = relationship(StudentAward, back_populates='student')
