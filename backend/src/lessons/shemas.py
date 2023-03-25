from pydantic import BaseModel


class LessonBase(BaseModel):
    content: str
