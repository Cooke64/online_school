from pydantic import BaseModel


class PollBase(BaseModel):
    title: str


class QuestionBase(BaseModel):
    question_text: str


class AnswerBase(BaseModel):
    answer_text: str
    is_correct: bool
