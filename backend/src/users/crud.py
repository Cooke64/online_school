from typing import Any

from sqlalchemy import and_

from src.database import BaseCrud
from src.students.models import Student
from .models import User, RolesType, Staff
from .shemas import UserCreate
from ..auth.models import Verification
from ..auth.utils.create_jwt import create_jwt
from ..auth.utils.hasher import get_password_hash, verify_password
from ..auth.utils.sending_mail import SendMail
from ..exceptions import NotFound, PermissionDenied
from ..teachers.models import Teacher


class UserCrud(BaseCrud, SendMail):

    @staticmethod
    def __update_userdata_and_get_phone(
            _dict: UserCreate
    ) -> tuple[dict[str], str]:
        """
        Удаляет из данных пользователя телефон,
        обновляет переданный пользователем пароль на хешированный.
        И возвращает телефон и обновленные данные пользователя.
        """
        dict_copy: dict = _dict.dict()
        phone = dict_copy.pop('phone')
        dict_copy.pop('password')
        dict_copy.update({'password': get_password_hash(_dict.password)})
        return dict_copy, phone

    @staticmethod
    def __get_role_type(user_type: RolesType):
        match user_type.value:
            case RolesType.teacher.value:
                role = RolesType.teacher.value
            case RolesType.student.value:
                role = RolesType.student.value
            case _:
                role = RolesType.staff.value
        return role

    def create_student_user(
            self, user_data: UserCreate,
    ) -> dict[str]:
        user_dict, phone = self.__update_userdata_and_get_phone(
            user_data
        )
        user = self.get_user(user_data.email)
        user_id = user.id
        if not user:
            new_user = User(**user_dict)
            user_id = self.create_item(new_user).id
        student = Student(
            phone=phone, user_id=user_id,
        )
        self.create_item(student)
        self.__create_and_send_verify_code(user_id, user_data.email)
        return user_dict

    def __create_and_send_verify_code(self, user_id: int, email: str):
        code = Verification(user_to_verify_id=user_id)
        item_in_bd: Verification = self.create_item(code)
        self._send_verification_mail(
            email,
            item_in_bd.link
        )
        print(item_in_bd.link)

    def __create_role_instanse(self, role: str, user: User) -> Any:
        user_id = user.id
        if role == RolesType.teacher.value:
            item = Teacher(user_id=user_id)
        elif role == RolesType.student.value:
            item = Student(user_id=user_id)
        else:
            item = Staff(user_id=user_id, staff_role=role)
            user.is_active = True
            self.session.commit()
        return item

    def create_user(self, user_type: RolesType, user_data: UserCreate) -> [dict[str]]:
        user_dict, *_ = self.__update_userdata_and_get_phone(
            user_data
        )
        role = self.__get_role_type(user_type)
        if self.get_user(user_data.email):
            raise PermissionDenied
        new_user_instanse = User(role=role, **user_dict)
        created_user = self.create_item(new_user_instanse)
        item = self.__create_role_instanse(user_type.value, created_user)
        self.create_item(item)
        self.__create_and_send_verify_code(created_user.id, created_user.email)
        return user_dict

    def verify_user(self, email: str, link: str):
        user: User = self.get_user(email)
        verify_user = self.session.query(Verification).filter(
            and_(
                Verification.link == link,
                Verification.user_to_verify_id == user.id
            )
        ).first()
        if not verify_user:
            raise NotFound
        user.is_active = True
        self.session.commit()

    def create_user_image(self):
        """Need to be done"""
        raise NotImplementedError

    def login_user(self, form_data):
        user = self.get_user(form_data.email)
        if not user or not verify_password(form_data.password, user.password):
            raise NotFound
        access_token = create_jwt(data={"sub": user.email})
        return {'Authorization': f'Bearer {access_token}'}
