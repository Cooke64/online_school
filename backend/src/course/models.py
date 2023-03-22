from sqlalchemy import Column as _, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Course(BaseModel):
    __tablename__ = 'courses'
    title = _(String(199), nullable=False)
    description = _(String, nullable=False)
    author_id = _(Integer, ForeignKey("users.id"))
    author = relationship("User", backref="courses", lazy=True)
    rating = _(Integer, default=5)


class Lesson(BaseModel):
    __tablename__ = 'lessons'
    body = _(String, nullable=False)
    course_id = _(Integer,
                  ForeignKey('courses.id', ondelete='CASCADE'),
                  nullable=False
                  )
