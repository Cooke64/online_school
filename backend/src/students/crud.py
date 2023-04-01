from typing import Any

from sqlalchemy import and_

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.students.models import StudentCourse, StudentPassedLesson
from src.users.models import User


class StudentCrud(BaseCrud):

    def get_students_courses(self, email: str) -> dict[str, User | Any]:
        user = self.get_user_by_email(User, email)
        purchased_courses = self.session.query(Course).join(
            StudentCourse).filter(and_(
                StudentCourse.student_id == user.student.id,
                StudentCourse.has_paid == True
        )
        ).all()

        passed = self.session.query(Lesson).join(
            StudentPassedLesson
        ).filter(StudentPassedLesson.student_id == user.student.id).all()

        return {
            'purchased_courses': purchased_courses,
            'lessons_passed': passed
        }
