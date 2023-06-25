from enum import Enum

import sqlalchemy as sa
from sqlalchemy.orm import relationship, backref

from src.BaseModel import BaseModel
from src.scripts.choice_field import ChoiceType


class RolesType(Enum):
    staff = 'Staff'
    student = 'Student'
    teacher = 'Teacher'


roles_as_dict = {i.name: i.value for i in RolesType}


class User(BaseModel):
    __tablename__ = 'users'
    first_name = sa.Column(sa.String(50), nullable=True)
    last_name = sa.Column(sa.String(99), nullable=True)
    username = sa.Column(sa.String(50), unique=True, nullable=True)
    email = sa.Column(sa.String(99), unique=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    is_active = sa.Column(sa.Boolean, default=False)
    role = sa.Column(ChoiceType(roles_as_dict), nullable=False,
                     default=RolesType.student.value)
    verify_code = relationship('Verification', back_populates='user_to_verify')
    user_image = relationship('UserProfileImage', back_populates='user', uselist=False)

    __table_args__ = (
        sa.PrimaryKeyConstraint('id', name='user_pk'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )


class StaffType(Enum):
    superuser = 'superuser'
    moderator = 'moderator'
    admin = 'admin'
    corrector = 'corrector'


staf_as_dict = {i.name: i.value for i in StaffType}


class Staff(BaseModel):
    __tablename__ = 'staffs'
    staff_role = sa.Column(ChoiceType(staf_as_dict), nullable=False,
                           default=StaffType.admin.value)
    user_id = sa.Column(sa.Integer, sa.ForeignKey('users.id'))
    user = relationship(User, backref=backref('staff', uselist=False))


class UserProfileImage(BaseModel):
    __tablename__ = 'users_profiles_images'
    photo_blob = sa.Column(sa.LargeBinary, nullable=False)
    photo_type = sa.Column(sa.String, nullable=True)
    user_id = sa.Column(
        sa.Integer, sa.ForeignKey('users.id'))
    user = relationship('User', back_populates='user_image')
