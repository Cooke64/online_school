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
