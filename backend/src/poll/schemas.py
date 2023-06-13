from pydantic import BaseModel

from src.utils.base_schemas import OrmBaseModel


class PollBase(BaseModel):
    poll_description: str | None


class QuestionBase(OrmBaseModel):
    question_text: str
    required_to_correct: int | None


class AnswerBase(OrmBaseModel):
    answer_text: str
    is_correct: bool


class ShowAnser(AnswerBase):
    id: int


class AddAnswers(OrmBaseModel):
    answers_list: list[AnswerBase]


class ShowQuestion(QuestionBase):
    id: int
    answers_list: list[ShowAnser]


class AddPoll(OrmBaseModel):
    poll_description: str | None
    question: QuestionBase
    answers: AddAnswers


class ShowLessonPoll(OrmBaseModel):
    id: int
    poll_description: str | None
    question_list: list[ShowQuestion]
