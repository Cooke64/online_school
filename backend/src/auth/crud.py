from .models import User
from src.database import BaseCrud
from .shemas import UserBase


class UserCrud(BaseCrud):
    def create_user(self, user_data: UserBase) -> None:
        news_item = User(**user_data.dict())
        self.create_item(news_item)
