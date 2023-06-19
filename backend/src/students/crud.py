from datetime import timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import Query, joinedload

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound
from src.students.models import StudentCourse, StudentPassedLesson


class StudentCrud(BaseCrud):
    def get_lessons_passed_by_user(self, student_id) -> Query:
        return self.session.query(Lesson).join(
            StudentPassedLesson
        ).options(
            joinedload(Lesson.course)).filter(
            StudentPassedLesson.student_id == student_id)

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

    def get_lessons_passed_today(self, student_id: int):
        query = self.get_lessons_passed_by_user(student_id)
        last_day = query.filter(
            StudentPassedLesson.when_pass == func.current_date()
        ).all()
        last_month = query.filter(
            StudentPassedLesson.when_pass >= func.current_date() - timedelta(
                days=30)
        ).all()
        return last_day, last_month

    def get_students_courses(self) -> dict:
        if not self.user:
            raise NotFound
        purchased_courses = self._get_purchased_courses(self.user.student.id)
        passsed_today, last_month = self.get_lessons_passed_today(
            self.user.student.id)
        return {
            'purchased_courses': purchased_courses,
            'pass_lessons_today': passsed_today,
            'pass_lessons_last_month': last_month,
            'left_comments': 123,
            'evalueted_courses': 123
        }

    def get_student_statistics(self):
        pass

    def get_passed_lessons(self):
        if not self.user:
            raise NotFound
        passsed_today, last_month = self.get_lessons_passed_today(
            self.user.student.id)
        return {
            'pass_lessons_today': passsed_today,
            'pass_lessons_last_month': last_month,
        }
