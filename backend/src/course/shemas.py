from datetime import datetime

from pydantic import BaseModel

from src.lessons.shemas import LessonBase
from src.teachers.shemas import ShowTeacherInCourseList
from src.utils.base_schemas import OrmBaseModel


class CourseBase(OrmBaseModel):
    title: str
    description: str
    is_free: bool = False


class CreateCourse(CourseBase):
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


class CoursePreview(OrmBaseModel):
    id: int
    photo_blob: str
    photo_type: str


class CourseListShow(OrmBaseModel):
    id: int
    title: str
    is_free: bool = False
    teachers: list[ShowTeacherInCourseList] | None
    reviews: list[ShowReview] | None
    course_preview: CoursePreview | None


class CourseInDetail(CourseBase):
    id: int
    created_at: datetime
    teachers: list[ShowTeacherInCourseList] | None
    lessons: list[LessonBase] | None
    course_preview: CoursePreview


class CourseDetail(BaseModel):
    course: CourseInDetail
    rating: int
    count_lessons: int


class Rating(BaseModel):
    rating: int
