from pydantic import BaseModel


class UserBase(BaseModel):
    staff_role: int
    firstname: str
    last_name: str
    username: str
    email: str
    password: str
    is_active: bool

    class Config:
        orm_mode = True
