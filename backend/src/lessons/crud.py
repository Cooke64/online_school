from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from src.auth.utils.auth_bearer import UserPermission
from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound, PermissionDenied
from src.lessons.shemas import LessonBase
from src.students.models import StudentCourse
from src.users.models import User


class LessonCrud(BaseCrud):
    def _get_user_course(self, course_id, student_id):
        user_course: StudentCourse = self.session.query(StudentCourse).filter(
            and_(
                StudentCourse.course_id == course_id,
                StudentCourse.student_id == student_id
            )
        ).first()
        return user_course

    def _create_lesson_instanse(self, course_id, lesson: LessonBase):
        new_lesson = Lesson(
            course_id=course_id,
            **lesson.dict()
        )
        result = self.create_item(new_lesson)
        return result

    def get_all_course_lessons(self, course_id):
        query: Course = self.session.query(Course).options(
            joinedload(Course.lessons)).where(
            Course.id == course_id).first()
        if query:
            return query
        raise NotFound

    def get_lesson_from_course(self, course_id, lessons_id, user_email):
        lesson: Lesson = self.session.query(Lesson).join(Course).filter(and_(
            Course.id == course_id, Lesson.id == lessons_id
        )).first()
        user = self.get_user_by_email(User, user_email)
        if not user or not lesson:
            raise NotFound
        user_course = self._get_user_course(course_id, user.student.id)
        if lesson.is_trial:
            return lesson
        if user_course and user_course.has_paid:
            return lesson
        raise PermissionDenied

    def add_lesson_to_course(
            self,
            course_id: int,
            lesson_data: LessonBase,
            permission: UserPermission

    ) -> None:
        if not permission.has_perm:
            raise PermissionDenied
        user: User = self.get_user_by_email(User, permission.user_email)
        course: Course = self.get_current_item(course_id, Course).first()
        if not user or not course:
            raise NotFound
        if user.teacher not in course.teachers:
            raise PermissionDenied
        if self.check_item_exists(course_id, Course):
            lesson = self._create_lesson_instanse(course.id, lesson_data)
            return lesson

    def make_lessone_done(self,  course_id, lessons_id, permission: UserPermission):
        user: User = self.get_user_by_email(User, permission.user_email)
        course: Course = self.get_current_item(course_id, Course).first()
        return 1
