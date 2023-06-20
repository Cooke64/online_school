from datetime import datetime
from enum import Enum

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
    """
    Модель Награда. Создается модератором или суперпользователем.
    Предназначена для создания системы наград пользователю. Создается по типу:
        - Award(name="Бог комментариев" column_name="coments" amount_to_get="300")
        - То есть для получения награды необходимо пользователю создать 300 комментариев к уроку.
    """
    __tablename__ = 'awards'
    # Название награды
    name = sa.Column(sa.String(199), nullable=False)
    # Поля фильтрации, по которому присваивается награда.
    column_name = sa.Column(sa.String(199), nullable=False)
    # Количество условных единиц для получения награды
    amount_to_get = sa.Column(sa.Integer, nullable=False)
    student_award = relationship(StudentAward, back_populates='award')


class AwardsTypes(Enum):
    comments = 'Comments'
    passed_lessons = 'PassedLessons'
    passed_by_day = 'PassedByDay'
