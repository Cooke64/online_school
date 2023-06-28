from pydantic import Field

from src.students_awards.shemas import ShowDetailAwards
from src.utils.base_schemas import OrmBaseModel


class UserCoursesShow(OrmBaseModel):
    title: str
    rating: int


class StudentShow(OrmBaseModel):
    username: str
    first_name: str | None = None
    last_name: str | None = None


class ShowUserProfile(OrmBaseModel):
    user: StudentShow
    courses: list[UserCoursesShow]
    phone: str | None


class ShowStudentData(OrmBaseModel):
    purchased_courses: list
    pass_lessons_today: list
    pass_lessons_last_month: list
    left_comments: int
    evalueted_courses: int
    awards: list[ShowDetailAwards]


class CourseTitle(OrmBaseModel):
    title: str = Field(None, alias='course_name')

    class Config:
        allow_population_by_field_name = True


class FavoriteLessons(OrmBaseModel):
    id: int
    title: str
    course: CourseTitle
