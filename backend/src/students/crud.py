from typing import Dict, Any

from sqlalchemy.orm import joinedload

from src.course.models import Course
from src.database import BaseCrud
from src.exceptions import NotFound
from src.students.models import StudentCourse
from src.users.models import User


class StudentCrud(BaseCrud):
    def get_student(self, email: str) -> User:
        query = self.session.query(User).filter(
            User.email == email
        ).first()
        return query

    def get_students_courses(self, email: str) -> dict[str, User | Any]:
        user = self.get_student(email)
        courses = self.session.query(Course).join(
            StudentCourse).filter(
            StudentCourse.student_id == user.student.id).all()
        return {
            'user': user,
            'courses': courses,
            'phone': user.student.phone
        }
