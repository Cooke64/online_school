from src.auth.utils.auth_bearer import UserPermission
from src.students.crud import StudentCrud
from src.students.models import Student
from src.users.models import User


class AwardCrud(StudentCrud):
    def __get_student_by_email(self, permission: UserPermission):
        student = self.session.query(
            Student).join(User).filter(
            User.email == permission.user_email).first()
        return student

    def get_student_comments(self, premission):
        if self.__get_student_by_email(premission):
            return 1
        return 0
