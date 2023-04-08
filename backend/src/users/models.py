from enum import Enum

from sqlalchemy import Column as _, String, Boolean, Integer, ForeignKey, \
    PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.scripts.choice_field import ChoiceType


class RolesType(Enum):
    staff = 'Staff'
    student = 'Student'
    teacher = 'Teacher'


roles_as_dict = {i.name: i.value for i in RolesType}


class User(BaseModel):
    __tablename__ = 'users'
    first_name = _(String(50), nullable=True)
    last_name = _(String(99), nullable=True)
    username = _(String(50), unique=True, nullable=True)
    email = _(String(99), unique=True, nullable=False)
    password = _(String, nullable=False)
    is_active = _(Boolean, default=False)
    role = _(ChoiceType(roles_as_dict), nullable=False,
             default=RolesType.student.value)
    verify_code = relationship('Verification', back_populates='user_to_verify')

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('username'),
        UniqueConstraint('email'),
    )


class StaffType(Enum):
    superuser = 'Superuser'
    moderator = 'Moderator'
    admin = 'Admin'
    corrector = 'Corrector'


staf_as_dict = {i.name: i.value for i in StaffType}


class Staff(BaseModel):
    __tablename__ = 'staffs'
    staff_role = _(ChoiceType(staf_as_dict), nullable=False,
                   default=StaffType.admin.value)
    user_id = _(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=backref('staff', uselist=False))
