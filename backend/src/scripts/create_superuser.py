from src.course.models import Course
from src.config import admin_data
from src.database import SessionLocal
from src.users.models import StaffType, Staff, User


def get_user(session, email):
    return session.query(User).filter(User.email == email).first()


def create_superuser():
    session = SessionLocal()
    staff_role = StaffType.superuser.value
    if get_user(session, admin_data.email):
        return 0
    user = User(
        is_active=True,
        **admin_data.dict()
    )
    session.add(user)
    session.commit()
    user_id = get_user(session, admin_data.email).id
    superuser = Staff(
        user_id=user_id,
        staff_role=staff_role
    )
    session.add(superuser)
    session.commit()
    return 1


def create_fake_courses():
    session = SessionLocal()
    for i in range(3):
        course = Course(
            title='title',
            description='description'
        )
        session.add(course)
        session.commit()


create_fake_courses()
