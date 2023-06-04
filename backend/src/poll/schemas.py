from pydantic import BaseModel

from src.utils.base_schemas import OrmBaseModel


class PollBase(BaseModel):
    title: str


class QuestionBase(BaseModel):
    question_text: str


class AnswerBase(OrmBaseModel):
    answer_text: str
    is_correct: bool


class AddAnswers(OrmBaseModel):
    answers_list: list[AnswerBase]
