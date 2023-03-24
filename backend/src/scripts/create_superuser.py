from src.auth.models import Staff, StaffType
from src.config import admin_data
from src.database import SessionLocal


def create_superuser():
    session = SessionLocal()
    try:
        superuser = Staff(
            staff_role=StaffType.superuser.value,
            is_active=True,
            **admin_data.dict()
        )

        session.add(superuser)
        session.commit()
    except Exception as e:
        raise e


create_superuser()
