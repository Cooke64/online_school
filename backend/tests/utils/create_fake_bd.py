from sqlalchemy.orm import Session

from src.course.models import Course

from tests.utils.crud import create_user, create_item, create_teacher
from tests.utils.users import UserData


def create_course(teacher, session: Session):
    course_data = {
        'title': 'title',
        'description': 'description',
    }
    for _ in range(3):
        new_item = Course(**course_data)
        new_item.teachers.append(teacher)
        create_item(new_item, session)


def create_fake_bd(session: Session):
    user_data = UserData('1@mail.ru', 'user1', '1234567')
    user = create_user(*user_data, session)
    teacher = create_teacher(user.id, session)
    create_course(teacher, session)
