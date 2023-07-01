from datetime import timedelta

from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound, PermissionDenied
from src.lessons.models import LessonComment
from src.students.models import StudentCourse, StudentPassedLesson, \
    FavoriteLesson, FavoriteCourse, Student
from src.users.models import User


class StudentCrud(BaseCrud):
    def _get_student_comments(self):
        student = self.user.student
        if student:
            return self.session.query(LessonComment).filter(
                LessonComment.student_id == student.id
            ).count()

    def _get_student_passed_lesson(self):
        student = self.user.student
        if student:
            return self.session.query(StudentPassedLesson).filter(
                StudentPassedLesson.student_id == student.id
            ).count()

    def _get_purchased_courses(self) -> list[StudentCourse]:
        """Получить список оплаченных курсов."""
        purchased_courses = self.session.query(Course).join(
            StudentCourse).filter(and_(
                StudentCourse.student_id == self.user.student.id,
                StudentCourse.has_paid == True
            )).all()
        return purchased_courses

    def get_lessons_passed_today(self):
        query = self.session.query(StudentPassedLesson)
        last_day = query.filter(
            StudentPassedLesson.when_pass == func.current_date()
        ).all()
        last_month = query.filter(
            StudentPassedLesson.when_pass >= func.current_date() - timedelta(
                days=30)
        ).all()
        return last_day, last_month

    def get_students_courses(self) -> dict:
        if not self.student:
            raise PermissionDenied
        purchased_courses = self._get_purchased_courses()
        passsed_today, last_month = self.get_lessons_passed_today()
        return {
            'purchased_courses': purchased_courses,
            'pass_lessons_today': passsed_today,
            'pass_lessons_last_month': last_month,
            'left_comments': self._get_student_comments(),
            'evalueted_courses': self._get_student_passed_lesson()
        }

    def get_passed_lessons(self):
        if not self.student:
            raise PermissionDenied
        passsed_today, last_month = self.get_lessons_passed_today()
        return {
            'pass_lessons_today': passsed_today,
            'pass_lessons_last_month': last_month,
        }

    def get_favorite_lessons(self):
        student = self.student
        query = self.session.query(Lesson).options(
            joinedload(Lesson.course)).join(FavoriteLesson).filter(
            FavoriteLesson.student_id == student.id
        ).all()
        return query

    def get_favorite_courses(self):
        student = self.student
        return student.favorite_courses
