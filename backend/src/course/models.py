from sqlalchemy import Column as _, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database import BaseModel
from src.teachers.models import Teacher


class Course(BaseModel):
    __tablename__ = 'courses'
    title = _(String(199), nullable=False)
    description = _(String, nullable=False)
    teacher_id = _(Integer, ForeignKey('teachers.id'))
    teacher = relationship(Teacher, backref='course_for_teacher')
    rating = _(Integer, default=5)
    lesson = relationship('Lesson', backref='course_for_lesson')

    course = relationship(
        'Student', secondary='student_courses',
        backref='course_for_student',
    )

    def __repr__(self) -> str:
        return f"Course(title={self.title!r}," \
               f"description={self.description!r}," \
               f"teacher_id={self.teacher_id!r}," \
               f"lesson={self.lesson!r}"


class Lesson(BaseModel):
    __tablename__ = 'lessons'
    title = _(String(199), nullable=False)
    content = _(Text, nullable=False)
    course_id = _(Integer,
                  ForeignKey('courses.id', ondelete='CASCADE'),
                  nullable=False
                  )

    def __repr__(self) -> str:
        return f'Lesson(id={self.id!r}'