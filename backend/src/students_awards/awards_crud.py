from src.students.crud import StudentCrud
from src.students.models import Student
from src.users.models import User


class AwardCrud(StudentCrud):
    def __get_student_by_email(self):
        student = self.session.query(
            Student).join(User).filter(
            User.email == self.user.email).first()
        return student

    def get_student_comments(self):
        if self.__get_student_by_email():
            return 1
        return 0
