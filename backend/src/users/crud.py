from sqlalchemy import and_

from src.database import BaseCrud
from src.students.models import Student
from .models import User, Staff, RolesType
from .shemas import UserCreate
from ..auth.models import Verification
from ..auth.utils.hasher import get_password_hash
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
    def __get_role_type(uesr_type):
        if uesr_type.value == RolesType.teacher.value:
            role = RolesType.teacher.value
        else:
            role = RolesType.student.value
        return role

    def get_all_users(self) -> list[User]:
        return self.session.query(User).join(Staff).all()

    def get_user(self, email: str) -> User:
        query = self.session.query(User).filter(User.email == email).first()
        return query

    def create_student_user(
            self, user_data: UserCreate,
    ) -> dict[str]:
        user_dict, phone = self.__update_userdata_and_get_phone(
            user_data
        )
        if not self.get_user(user_data.email):
            new_user = User(**user_dict)
            self.create_item(new_user)
        user_id = self.get_user(user_data.email)
        student = Student(
            phone=phone, user_id=user_id.id,
        )
        self.create_item(student)
        self.__create_and_send_verification_letter(user_id.id)
        return user_dict

    def __create_and_send_verification_letter(self, user_id, email):
        code = Verification(
            user_to_verify_id=user_id
        )
        item_in_bd: Verification = self.create_item(code)
        self._send_verification_mail(
            email,
            item_in_bd.link
        )
        print(item_in_bd.link)

    def create_user(self, user_type, user_data: UserCreate) -> [
            dict[str]]:
        user_dict, *_ = self.__update_userdata_and_get_phone(
            user_data
        )
        user = self.get_user(user_data.email)
        if user:
            raise PermissionDenied
        if not self.get_user(user_data.email):
            new_user = User(
                role=self.__get_role_type(user_type),
                **user_dict)
            user_id = self.create_item(new_user)
            if user_type == RolesType.teacher.value:
                item = Teacher(user_id=user_id.id)
            else:
                item = Student(user_id=user_id.id)
            self.create_item(item)
            self.__create_and_send_verification_letter(
                user.email, user.id
            )
        return user_dict

    def verify_user(self, email: str, link: str):
        user: User = self.get_user_by_email(User, email)
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
        pass