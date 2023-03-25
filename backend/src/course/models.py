from sqlalchemy import Column as _, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Course(BaseModel):
    __tablename__ = 'courses'
    title = _(String(199), nullable=False)
    description = _(String, nullable=False)
    rating = _(Integer, default=5)
    lesson = relationship('Lesson', backref='course')


class Lesson(BaseModel):
    __tablename__ = 'lessons'
    title = _(String(199), nullable=False)
    content = _(Text, nullable=False)
    course_id = _(Integer,
                  ForeignKey('courses.id', ondelete='CASCADE'),
                  nullable=False
                  )
