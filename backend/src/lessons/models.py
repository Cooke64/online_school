from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.BaseModel import BaseModel


class LessonComment(BaseModel):
    __tablename__ = 'lesson_comments'
    student_id = sa.Column(sa.Integer, sa.ForeignKey('students.id'))
    lesson_id = sa.Column(sa.Integer, sa.ForeignKey('lessons.id'))
    lesson = relationship('Lesson', back_populates='lesson_comment')
    student = relationship('Student', back_populates='lesson_comment')

    text = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False,
                           default=datetime.utcnow)


