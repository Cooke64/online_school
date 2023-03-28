from enum import Enum
from typing import Dict

import bcrypt
from jose import jwt
from sqlalchemy import Column as _, String, Boolean, Integer, ForeignKey, \
    PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship, backref

from src.database import BaseModel
from src.scripts.choice_field import ChoiceType


class User(BaseModel):
    __tablename__ = 'users'
    first_name = _(String(50), nullable=True)
    last_name = _(String(99), nullable=True)
    username = _(String(50), unique=True, nullable=True)
    email = _(String(99), unique=True, nullable=False)
    password = _(String, nullable=False)
    is_active = _(Boolean, default=False)

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
    staff_role = _(ChoiceType(staf_as_dict), nullable=False, default=StaffType.admin.value)
    user_id = _(Integer, ForeignKey('users.id'))
    user = relationship(User, backref=backref('staff', uselist=False))

