from pydantic import BaseModel, EmailStr, Field, constr, validator

from src.users.models import RolesType
from src.utils.base_schemas import OrmBaseModel


class UserBase(BaseModel):
    email: EmailStr


class StaffShow(OrmBaseModel):
    username: str
    staff_role: str


class UserCreate(OrmBaseModel):
    username: constr(regex="^[A-Za-z0-9-_]+$", to_lower=True, strip_whitespace=True)
    first_name: str = Field(min_length=1, max_length=128)
    last_name: str = Field(min_length=1, max_length=128)
    email: str
    password: str
    phone: str | None

    class Config:
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

    @validator('username')
    def validate_username(cls, username: str):
        if username == 'me':
            raise ValueError('Надо выбрать другоеr')
        return username


class UserLogin(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "2@2.com",
                "password": "2"
            }
        }


class UserCreateShowResult(UserBase):
    username: str


class UserShowProfile(OrmBaseModel):
    username: str
    first_name: str
    last_name: str
    role: RolesType
    is_active: bool
    email: str
