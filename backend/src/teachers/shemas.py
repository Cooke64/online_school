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
    user: TeacherData


class TeacherStatistics(OrmBaseModel):
    count_courses: int
    total_reviews: int
    total_rating: float


class TeacherShow(TeacherStatistics):
    teacher_info: TeacherInfo


class ShowCourse(OrmBaseModel):
    title: str
    description: str
    is_free: bool = False


class TeacherInfoDetail(OrmBaseModel):
    id: int
    description: str | None
    user: TeacherData
    courses: list[ShowCourse]


class TeacherShowDetail(TeacherStatistics):
    teacher_info: TeacherInfoDetail
