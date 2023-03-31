

from pydantic import BaseModel, Field


class TeacherData(BaseModel):
    username: str

    class Config:
        orm_mode = True


class ShowTeacherInCourseList(BaseModel):
    description: str | None
    user: TeacherData = Field(alias='user_data')

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
