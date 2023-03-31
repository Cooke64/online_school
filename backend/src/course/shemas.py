from pydantic import BaseModel

from src.lessons.shemas import LessonBase
from src.teachers.shemas import ShowTeacherInCourseList


class CourseBase(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True


class CreateCourse(CourseBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'title',
                'description': 'description',
            }
        }
        orm_mode = True


class CourseShow(CourseBase):
    teacher: list | None = []


class CourseShowRating(BaseModel):
    course: CourseShow
    rating: float


class UpdateCourse(BaseModel):
    title: str | None
    description: str | None


class CourseListShow(BaseModel):
    id: int
    title: str
    teachers: list[ShowTeacherInCourseList] | None

    class Config:
        orm_mode = True
