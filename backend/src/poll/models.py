import sqlalchemy as sa
from sqlalchemy.orm import relationship

from src.database import BaseModel


class Poll(BaseModel):
    """Модель, представляющая опрос к уроку.
    Связана с уроком one to one, с таблицей Questions, где находятся ответы.
    """
    __tablename__ = 'polls'
    title = sa.Column(sa.String(199), nullable=False)
    lesson_id = sa.Column(sa.Integer, sa.ForeignKey('lessons.id'))
    lesson = relationship('Lesson', back_populates='lesson_poll')
    question_list = relationship('Question', back_populates='poll')


class Question(BaseModel):
    __tablename__ = 'questions'
    poll_id = sa.Column(sa.Integer, sa.ForeignKey('polls.id'))
    poll = relationship('Poll', back_populates='question_list')
    question_text = sa.Column(sa.Text, nullable=False)
    answers_list = relationship('Answer', back_populates='question')


class Answer(BaseModel):
    __tablename__ = 'answers'
    question_id = sa.Column(sa.Integer, sa.ForeignKey('questions.id'))
    question = relationship('Question', back_populates='answers_list')
    answer_text = sa.Column(sa.Text, nullable=False)
    is_correct = sa.Column(sa.Boolean, nullable=False, default=False)
