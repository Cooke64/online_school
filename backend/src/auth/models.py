from enum import Enum

from sqlalchemy import Column as _, String, Boolean

from src.database import BaseModel
from src.scripts.choice_field import ChoiceType


class User(BaseModel):
    __abstract__ = True
    first_name = _(String(50), unique=True, nullable=False)
    last_name = _(String(99), unique=True, nullable=True)
    username = _(String(50), unique=True, nullable=True)
    email = _(String(99), unique=True, nullable=False)
    password = _(String, nullable=False)
    is_active = _(Boolean, default=False)


class StaffType(Enum):
    superuser = 'Superuser'
    moderator = 'Moderator'
    admin = 'Admin'
    corrector = 'Corrector'


staf_as_dict = {i.name: i.value for i in StaffType}


class Staff(User):
    __tablename__ = 'staffs'
    staff_role = _(ChoiceType(staf_as_dict), nullable=False, default=StaffType.admin.value)

    def __repr__(self) -> str:
        return f'Staff(staff_role={self.staff_role!r}'
