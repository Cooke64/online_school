from datetime import datetime

from src.utils.base_schemas import OrmBaseModel


class LessonBase(OrmBaseModel):
    id: int | None
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


class CommentBase(OrmBaseModel):
    text: str


class UserComment(OrmBaseModel):
    id: int
    username: str


class StudentInComment(OrmBaseModel):
    user: UserComment


class CommentInLesson(CommentBase):
    id: int
    lesson_id: int
    student_id: int
    student: StudentInComment
    created_at: datetime


class LessonDetail(LessonBase):
    photos: list
    videos: list
    lesson_comment: list[CommentInLesson]


class ShowLessonDetail(OrmBaseModel):
    count_lessons: int
    lesson: LessonDetail
    lesson_teachers: list[str]
