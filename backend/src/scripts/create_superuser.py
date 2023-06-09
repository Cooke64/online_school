from src.config import admin_data
from src.course.models import Course
from src.main_crud import SessionLocal
from src.users.models import StaffType, Staff, User, RolesType


def get_user(session, email):
    return session.query(User).filter(User.email == email).first()


def create_superuser():
    session = SessionLocal()
    staff_role = StaffType.superuser.value
    if get_user(session, admin_data.email):
        return 0
    user = User(
        is_active=True,
        staff_role=RolesType.staff,
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
            title=f'title{i}',
            description=f'description {i}'
        )
        session.add(course)
        session.commit()


# create_superuser()
create_fake_courses()
