from src.database import BaseCrud
from src.exceptions import NotFound
from src.students.models import StudentCourse
from src.users.models import User


class StudentCrud(BaseCrud):
    def get_student(self, email: str) -> User | NotFound:
        query = self.session.query(User).filter(
            User.email == email
        ).first()
        return query

    def get_students_courses(self, email):
        user_id = self.get_student(email).student.id
        return self.session.query(StudentCourse).filter(
            StudentCourse.student_id == user_id
        ).all()

    def add_course_to_stident(self, email):
        user_id = self.get_student(email).id
