from pydantic import BaseModel


class LessonBase(BaseModel):
    title: str
    content: str

    class Config:
        orm_mode = True