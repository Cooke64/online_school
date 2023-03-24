from pydantic import BaseModel, EmailStr


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

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'user',
                'first_name': 'firstname',
                'last_name': 'last_name',
                'email': 'email@mail.com',
                'password': 'password'
            }
        }


class UserLogin(UserBase):
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'email': 'email@mail.com',
                'password': 'password'
            }
        }