from pydantic import BaseModel, Field

from src.lessons.shemas import LessonBase
from src.teachers.shemas import ShowTeacherInCourseList


class CourseBase(BaseModel):
    title: str
    description: str
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


class CourseListShow(BaseModel):
    title: str
    lessons: list[LessonBase] | None
    teachers: list[ShowTeacherInCourseList] | None

    class Config:
        orm_mode = True
