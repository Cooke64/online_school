from sqlalchemy import Column as _, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Course(BaseModel):
    __tablename__ = 'courses'
    title = _(String(199), nullable=False)
    description = _(String, nullable=False)
    teacher = relationship(
        'Teacher',
        secondary='teacher_courses',
        back_populates='course'
    )
    rating = _(Integer, default=5)
    lesson = relationship('Lesson', backref='course_for_lesson')

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
