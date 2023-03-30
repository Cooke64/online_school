from src.auth.utils.create_jwt import create_jwt
from src.database import BaseCrud
from src.students.models import Student
from .models import User, Staff, RolesType
from .shemas import UserCreate
from ..auth.utils.hasher import get_password_hash
from ..teachers.models import Teacher


class UserCrud(BaseCrud):

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

    def get_all_users(self) -> list[User]:
        return self.session.query(User).join(Staff).all()

    def get_user(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

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
        return user_dict

    def create_teacher_user(
            self, user_data: UserCreate,
    ) -> dict[str]:
        user_dict, *_ = self.__update_userdata_and_get_phone(
            user_data
        )
        if not self.get_user(user_data.email):
            new_user = User(
                role=RolesType.teacher.value,
                **user_dict)
            self.create_item(new_user)

        user_id = self.get_user(user_data.email)
        if RolesType.teacher.value:
            item = Teacher(
                user_id=user_id.id,
            )
        else:
            item = Student(
                user_id=user_id.id,
            )
        self.create_item(item)
        return user_dict
