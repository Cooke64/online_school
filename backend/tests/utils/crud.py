from sqlalchemy.orm import Session

from src.auth.utils.hasher import get_password_hash
from src.students.models import Student
from src.teachers.models import Teacher
from src.users.models import User, RolesType


def create_item(data, session: Session):
    session.add(data)
    session.commit()
    session.refresh(data)
    return data


def create_user(
        email,
        username,
        password,
        session: Session,
        is_teacher=True
        ):
    role = RolesType.teacher.value if is_teacher else RolesType.student.value
    user_data = User(
        email=email,
        username=username,
        first_name=username,
        last_name=username,
        password=get_password_hash(password),
        role=role,
    )
    return create_item(user_data, session)


def get_user_by_email(email: str, session: Session):
    return session.query(User).filter(User.email == email).first()


def create_teacher(user_id: int, session: Session):
    new_teacher = Teacher(user_id=user_id)
    create_item(new_teacher, session)


def create_student(user_id: int, session: Session):
    new_student = Student(user_id=user_id)
    create_item(new_student, session)
