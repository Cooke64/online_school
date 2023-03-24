from src.database import BaseCrud
from .models import User, Role
from .shemas import UserCreate
from src.students.models import Student


class UserCrud(BaseCrud):

    def get_user(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def create_role(self, user_id):
        role_id = self.session.query(Role).filter(
            Role.user_id == user_id).first()
        if not role_id:
            role = Role(user_id=user_id.id)
            self.create_item(role)

    def create_student_user(self, user_data: UserCreate) -> None:
        if not self.get_user(user_data.email):
            new_user = User(**user_data.dict())
            self.create_item(new_user)
        user_id = self.get_user(user_data.email)
        new_role = Role(user_id=user_id.id)
        self.create_item(new_role)
        role = self.session.query(Role).filter(
            Role.user_id == user_id.id).first()
        student = Student(role_id=role.id, phone='1234')
        self.create_item(student)
