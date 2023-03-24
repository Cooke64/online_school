from enum import Enum

from sqlalchemy import Column as _, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.scripts.choice_field import ChoiceType


class User(BaseModel):
    __tablename__ = 'users'
    first_name = _(String(50), unique=True, nullable=False)
    last_name = _(String(99), unique=True, nullable=False)
    username = _(String(50), unique=True, nullable=True)
    email = _(String(99), unique=True, nullable=False)
    password = _(String, nullable=False)
    is_active = _(Boolean, default=False)
    shool_role = relationship('Role', back_populates='user')

    def __repr__(self) -> str:
        return f'User(id={self.id!r})'


class Role(BaseModel):
    __tablename__ = 'rols'
    user_id = _(Integer, ForeignKey('users.id'))
    user = relationship(User, back_populates='shool_role')

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}," \
               f" user={self.user!r}," \
               f" user_id={self.user_id!r})"


class StaffType(Enum):
    superuser = 'Superuser'
    moderator = 'Moderator'
    admin = 'Admin'
    corrector = 'Corrector'


staf_as_dict = {i.name: i.value for i in StaffType}


class Staff(BaseModel):
    __tablename__ = 'staffs'
    staff_role = _(ChoiceType(staf_as_dict), nullable=False, default=StaffType.admin.value)
    role_id = _(Integer, ForeignKey('rols.id'))
    role = relationship(Role, backref=backref('staff', uselist=False))

    def __repr__(self) -> str:
        return f'Staff(staff_role={self.staff_role!r}'
