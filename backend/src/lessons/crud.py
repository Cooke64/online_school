from typing import Dict, Any

from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload

from src.auth.utils.auth_bearer import UserPermission
from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound, PermissionDenied
from src.lessons.models import LessonComment
from src.lessons.shemas import LessonBase, CommentBase
from src.students.models import StudentCourse, StudentPassedLesson, Student
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

    def get_lesson_from_course(
            self,
            course_id: int,
            lessons_id: int,
            permission: UserPermission) -> dict:
        lesson: Lesson = self.session.query(Lesson).options(
            joinedload(Lesson.lesson_comment).options(joinedload(
                LessonComment.student
            ).options(joinedload(Student.user)))).options(
            joinedload(Lesson.photos)).options(
            joinedload(Lesson.videos)).filter(and_(
                Lesson.course_id == course_id, Lesson.id == lessons_id
            )).first()
        count_lessons = self.session.query(Lesson).filter(Lesson.course_id == course_id).count()
        if lesson and lesson.is_trial or permission.role == 'Teacher':
            return {'lesson': lesson, 'count_lessons': count_lessons}
        user = self.get_user_by_email(User, permission.user_email)
        if not user:
            raise PermissionDenied
        user_course = self._get_user_course(course_id, user.student.id)
        if user_course and user_course.has_paid:
            return {'lesson': lesson, 'count_lessons': count_lessons}
        raise PermissionDenied

    def add_lesson_to_course(
            self,
            course_id: int,
            lesson_data: LessonBase,
            permission: UserPermission

    ) -> None:
        user: User = self.get_user_by_email(User, permission.user_email)
        course: Course = self.get_current_item(course_id, Course).first()
        if not user or not course:
            raise NotFound
        if user.teacher not in course.teachers:
            raise PermissionDenied
        if self.check_item_exists(course_id, Course):
            # self._create_lesson_instanse(course.id, lesson_data)
            descending = self.session.query(Lesson).filter(
                Lesson.course_id == course_id
            ).order_by(Lesson.id.desc())
            return descending.first().id

    def make_lessone_done(
            self,
            lessons_id: int,
            permission: UserPermission
    ) -> StudentPassedLesson | None:
        user: User = self.get_user_by_email(User, permission.user_email)
        passed_lesson: StudentPassedLesson = self.session.query(
            StudentPassedLesson).filter(
            student_id=user.student.id,
            lesson_id=lessons_id,
        ).first()
        if not passed_lesson:
            raise NotFound
        passed_lesson.when_pass = func.now()
        passed_lesson.has_pass = True
        self.session.commit()
        return passed_lesson

    def add_comment_to_lesson(
            self,
            text: CommentBase,
            lesson_id: int,
            course_id: int,
            permission: UserPermission,

    ):
        """Добавить отзыв на урок."""
        lesson = self.session.query(Lesson).filter(
            and_(Lesson.id == lesson_id, Lesson.course_id == course_id)
        ).first()
        student = self.session.query(
            Student).join(User).filter(
            User.email == permission.user_email
        ).first()
        new_comment = LessonComment(
            student_id=student.id,
            lesson_id=lesson.id,
            text=text.text
        )
        self.create_item(new_comment)

    def remove_comment_from_lesson(
            self, comment_id: int, lesson_id: int,
            permission: UserPermission):
        student = self.session.query(
            Student).join(User).filter(
            User.email == permission.user_email
        ).first()
        comment = self.session.query(LessonComment).filter(
            and_(
                LessonComment.student_id == student.id,
                LessonComment.lesson_id == lesson_id,
                LessonComment.id == comment_id

            )
        ).first()
        if not comment:
            raise NotFound
        self.remove_item(comment.id, LessonComment)
