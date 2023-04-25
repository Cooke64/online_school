from pydantic import Field

from src.utils.base_schemas import OrmBaseModel


class TeacherData(OrmBaseModel):
    username: str


class ShowTeacherInCourseList(OrmBaseModel):
    description: str | None
    user: TeacherData = Field(alias='user_data')

    class Config:
        allow_population_by_field_name = True


class TeacherInfo(OrmBaseModel):
    id: int
    description: str | None


class ShowTeachersList(OrmBaseModel):
    userdata: TeacherData
    teacher_info: TeacherInfo
    count_courses: int
    total_reviews: int
    total_rating: float
