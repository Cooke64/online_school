from src.database import BaseCrud
from .models import User, Staff
from .shemas import UserCreate


class UserCrud(BaseCrud):

    def get_all_users(self):
        return self.session.query(User).join(Staff).all()

    def get_user(self, email):
        return self.session.query(User).filter(User.email == email).first()

    def create_student_user(self, user_data: UserCreate) -> None:
        if not self.get_user(user_data.email):
            new_user = User(**user_data.dict())
            self.create_item(new_user)
