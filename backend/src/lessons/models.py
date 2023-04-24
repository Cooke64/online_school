from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import UniqueConstraint
from sqlalchemy.orm import relationship

from src.database import BaseModel


class LessonComment(BaseModel):
    __tablename__ = 'lesson_comments'
    __table_args__ = (
        UniqueConstraint('student_id', 'course_id'),
    )
    student_id = sa.Column(sa.Integer, sa.ForeignKey('students.id'))
    lesson_id = sa.Column(sa.Integer, sa.ForeignKey('courses.id'))
    text = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False,
                           default=datetime.utcnow)
    lesson = relationship('Course', back_populates='reviews')
    student = relationship('Student', back_populates='lesson_comment')

