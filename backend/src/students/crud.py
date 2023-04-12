from datetime import timedelta
from typing import Any

from sqlalchemy import and_, func
from sqlalchemy.orm import Query, joinedload

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.students.models import StudentCourse, StudentPassedLesson
from src.users.models import User


class StudentCrud(BaseCrud):
    def get_lessons_passed_by_user(self, student_id) -> Query:
        return self.session.query(Lesson).join(
            StudentPassedLesson
        ).filter(StudentPassedLesson.student_id == student_id)

    def _get_purchased_courses(
            self, student_id: int) -> list[StudentCourse]:
        """Получить список оплаченных курсов."""
        purchased_courses = self.session.query(Course).join(
            StudentCourse).filter(and_(
                StudentCourse.student_id == student_id,
                StudentCourse.has_paid == True
        )).all()
        return purchased_courses

    def _get_passed_lessons(self, student_id: int, course_id: int = 1) -> list[
            StudentPassedLesson]:
        """Получить список пройденныйх уроков в курсе"""
        query = self.get_lessons_passed_by_user(student_id)
        return query.all()

    def _get_lessons_passed_today(self, student_id: int):
        query = self.get_lessons_passed_by_user(student_id)
        last_day = query.filter(
            StudentPassedLesson.when_pass == func.current_date()
        ).count()
        last_month = query.filter(
            StudentPassedLesson.when_pass >= func.current_date() - timedelta(
                days=30)
        ).count()
        return last_day, last_month

    def get_course_progress(self, students_id):
        q = self.session.query(Lesson).join(Course).join(StudentPassedLesson).filter(
            and_(
                Course.id == 1,
                StudentPassedLesson.student_id == students_id
            )
        ).all()
        res = {}
        for course in q:
            res[course.course.title] = q
        return res

    def get_students_courses(self, email: str) -> dict[str, User | Any]:
        user = self.get_user_by_email(User, email)
        purchased_courses = self._get_purchased_courses(user.student.id)
        passsed_today, last_month = self._get_lessons_passed_today(
            user.student.id)
        progress = self.get_course_progress(user.student.id)
        return {
            'purchased_courses': purchased_courses,
            'pass_lessons_today': passsed_today,
            'pass_lessons_last_month': last_month,
            'progres': progress
        }
