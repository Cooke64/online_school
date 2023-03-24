from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class StaffShow(UserBase):
    staff_role: str
    firstname: str | None = None
    last_name: str | None = None
    email: str
    password: str
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: str
    password: str

    class Config:
        orm_mode = True
