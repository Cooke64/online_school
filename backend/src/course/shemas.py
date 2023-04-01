from pydantic import BaseModel

from src.lessons.shemas import LessonBase
from src.teachers.shemas import ShowTeacherInCourseList


class CourseBase(BaseModel):
    title: str
    description: str
    is_free: bool = False

    class Config:
        orm_mode = True


class CreateCourse(CourseBase):
    class Config:
        schema_extra = {
            'example': {
                'title': 'title',
                'description': 'description',
                'is_free': False
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
    is_free: bool = False
    teachers: list[ShowTeacherInCourseList] | None

    class Config:
        orm_mode = True


class CourseInDetail(CourseBase):
    teachers: list[ShowTeacherInCourseList] | None
    lessons: list[LessonBase] | None


class CourseDetail(BaseModel):
    course: CourseInDetail
    rating: int
