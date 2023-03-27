from pydantic import BaseModel

from src.users.shemas import UserBase


class UserCoursesShow(BaseModel):
    title: str
    rating: int

    class Config:
        orm_mode = True


class StudentShow(UserBase):
    username: str
    first_name: str | None = None
    last_name: str | None = None

    class Config:
        orm_mode = True


class ShowUserProfile(BaseModel):
    user: StudentShow
    courses: list[UserCoursesShow]
    phone: str | None

    class Config:
        orm_mode = True
