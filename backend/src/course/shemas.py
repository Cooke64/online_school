from pydantic import BaseModel, Field

from src.lessons.shemas import LessonBase


class CourseBase(BaseModel):
    title: str
    description: str
    # teacher_id: int
    rating: int

    class Config:
        orm_mode = True


class CourseShow(CourseBase):
    pass


class CreateCourse(CourseBase):
    rating: int = Field(
        gt=0, le=5,
        title='The rating of the current curse',
        description='The rating must be greater than zero and equal or less than five'
    )

    class Config:
        schema_extra = {
            'example': {
                'title': 'title',
                'description': 'description',
                'rating': 4
            }
        }
        orm_mode = True


class CourseShowDetail(CourseBase):
    id: int
    lessons: list[LessonBase] | None = []


class UpdateCourse(BaseModel):
    title: str | None
    description: str | None
    rating: int | None
