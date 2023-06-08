from pydantic import BaseModel

from src.utils.base_schemas import OrmBaseModel


class PollBase(BaseModel):
    title: str


class QuestionBase(BaseModel):
    question_text: str


class AnswerBase(OrmBaseModel):
    answer_text: str
    is_correct: bool


class ShowAnser(AnswerBase):
    id: int


class AddAnswers(OrmBaseModel):
    answers_list: list[AnswerBase]


class ShowQuestion(OrmBaseModel):
    id: int
    question_text: str
    answers_list: list[ShowAnser]


class ShowLessonPoll(OrmBaseModel):
    id: int
    question_list: list[ShowQuestion]
