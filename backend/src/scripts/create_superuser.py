from src.config import admin_data
from src.database import SessionLocal
from src.users.models import StaffType, Staff, User, Role


def get_user(session, email):
    return session.query(User).filter(User.email == email).first()


def create_superuser():
    session = SessionLocal()
    staff_role = StaffType.superuser.value
    user = get_user(session, admin_data.email)
    if user:
        return 0
    user = User(
        is_active=True,
        **admin_data.dict()
    )
    session.add(user)
    session.commit()
    user_id = get_user(session, admin_data.email).id
    role_super = Role(
        user_id=user_id
    )
    session.add(role_super)
    session.commit()
    role_id = session.query(Role).filter(Role.user_id == user_id).first().id
    superuser = Staff(
        role_id=role_id,
        staff_role=staff_role
    )
    session.add(superuser)
    session.commit()
    return 1


print(create_superuser())
