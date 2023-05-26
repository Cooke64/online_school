import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Poll(BaseModel):
    """Модель, представляющая опрос к уроку.
    Связана с уроком, с таблицей Questions, где находятся ответы.
    """
    __tablename__ = 'polls'
    title = sa.Column(sa.String(199), nullable=False)
    # lesson_id = sa.Column(sa.Integer, sa.ForeignKey('lessons.id'))
    # lesson = relationship('Lesson', back_populates='polls')
    question_list = relationship('LessonPhoto', back_populates='lesson_content')


class Question(BaseModel):
    __tablename__ = 'questions'
    poll_id = sa.Column(sa.Integer, sa.ForeignKey('polls.id'))
    poll = relationship('Poll', back_populates='question_list')
    text = sa.Column(sa.Text, nullable=False)
    is_correct = sa.Column(sa.Boolean, nullable=False, default=False)
