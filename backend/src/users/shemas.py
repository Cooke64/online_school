from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class StaffShow(UserBase):
    username: str
    staff_role: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    username: str
    first_name: str | None = None
    last_name: str | None = None
    password: str
    phone: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'user',
                'first_name': 'firstname',
                'last_name': 'last_name',
                'email': 'email@mail.com',
                'password': 'password',
                'phone': '12345678'
            }
        }


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "1223@mail.ru",
                "password": "password"
            }
        }


class UserCreateShowResult(UserBase):
    username: str

