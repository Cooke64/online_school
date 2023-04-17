from src.utils.base_schemas import OrmBaseModel


class LessonBase(OrmBaseModel):
    title: str
    content: str
    is_trial: bool = False

    class Config:
        schema_extra = {
            'example': {
                'title': 'The title of the lesson',
                'content': 'Some description',
                'is_trial': False
            }
        }
