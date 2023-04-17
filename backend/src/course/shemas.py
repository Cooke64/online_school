from pydantic import BaseModel

from src.lessons.shemas import LessonBase
from src.teachers.shemas import ShowTeacherInCourseList
from src.utils.base_schemas import OrmBaseModel


class CourseBase(OrmBaseModel):
    title: str
    description: str
    is_free: bool = False


class CreateCourse(OrmBaseModel):
    class Config:
        schema_extra = {
            'example': {
                'title': 'title',
                'description': 'description',
                'is_free': False
            }
        }


class CourseShow(CourseBase):
    teacher: list | None = []


class CourseShowRating(BaseModel):
    course: CourseShow
    rating: float


class UpdateCourse(BaseModel):
    title: str | None
    description: str | None


class ReviewBase(BaseModel):
    text: str


class ShowReview(OrmBaseModel):
    id: int


class CourseListShow(OrmBaseModel):
    id: int
    title: str
    is_free: bool = False
    teachers: list[ShowTeacherInCourseList] | None
    reviews: list[ShowReview] | None


class CourseInDetail(CourseBase):
    teachers: list[ShowTeacherInCourseList] | None
    lessons: list[LessonBase] | None


class CourseDetail(BaseModel):
    course: CourseInDetail
    rating: int
