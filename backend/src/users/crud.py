from src.database import BaseCrud
from src.students.models import Student
from .models import User, Staff
from .shemas import UserCreate


class UserCrud(BaseCrud):

    def __update_userdata_and_get_phone(
            self, _dict: UserCreate, hashed_password: str
    ) -> tuple[dict[str], str]:
        """
        Удаляет из данных пользователя телефон,
        обновляет переданный пользователем пароль на хешированный.
        И возвращает телефон и обновленные данные пользователя.
        """
        dict_copy: dict = _dict.dict()
        phone = dict_copy.pop('phone')
        dict_copy.pop('password')
        dict_copy.update({'password': hashed_password})
        return dict_copy, phone

    def get_all_users(self) -> list[User]:
        return self.session.query(User).join(Staff).all()

    def get_user(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def create_student_user(
            self, user_data: UserCreate,
            haashed_password: str,
    ) -> None:
        user_dict, phone = self.__update_userdata_and_get_phone(
            user_data, haashed_password
        )
        if not self.get_user(user_data.email):
            new_user = User(**user_dict)
            self.create_item(new_user)
        user_id = self.get_user(user_data.email)
        student = Student(
            phone=phone, user_id=user_id.id,
        )
        self.create_item(student)
