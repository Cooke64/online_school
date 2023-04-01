from pydantic import BaseModel


class LessonBase(BaseModel):
    title: str
    content: str
    is_trial: bool = False

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'The title of the lesson',
                'content': 'Some description',
                'is_trial': False
            }
        }