from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.BaseModel import BaseModel


class StudentAward(BaseModel):
    __tablename__ = 'student_awards'
    __table_args__ = (
        sa.UniqueConstraint('student_id', 'award_id'),
    )
    student_id = sa.Column(sa.Integer, sa.ForeignKey('students.id'))
    award_id = sa.Column(sa.Integer, sa.ForeignKey('awards.id'))
    when_get = sa.Column(sa.DateTime, nullable=False, default=datetime.utcnow)
    student = relationship('Student', back_populates='student_award')
    award = relationship('Award', back_populates='student_award')


class Award(BaseModel):
    __tablename__ = 'awards'
    name = sa.Column(sa.String(199), nullable=False)
    status = sa.Column(sa.Text, nullable=False)
    student_award = relationship(StudentAward, back_populates='award')


