from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound, PermissionDenied
from src.lessons.models import LessonComment
from src.lessons.shemas import LessonBase, CommentBase
from src.students.models import StudentCourse, StudentPassedLesson, Student
from src.teachers.models import Teacher


class LessonCrud(BaseCrud):
    def _get_user_course(self, course_id, student_id):
        user_course: StudentCourse = self.session.query(StudentCourse).filter(
            and_(
                StudentCourse.course_id == course_id,
                StudentCourse.student_id == student_id
            )
        ).first()
        return user_course

    def _create_lesson_instanse(self, course_id, lesson: LessonBase) -> Lesson:
        new_lesson = Lesson(
            course_id=course_id,
            **lesson.dict()
        )
        return self.create_item(new_lesson)

    def get_all_course_lessons(self, course_id):
        query: Course = self.session.query(Course).options(
            joinedload(Course.lessons)).where(
            Course.id == course_id).first()
        if query:
            return query
        raise NotFound

    def __check_leesson_for_user(self, lesson: Lesson, course_id: int) -> None:
        user_type = self.is_teacher or self.is_staff
        is_trial = lesson and lesson.is_trial or user_type
        if not is_trial:
            raise PermissionDenied
        user = self.user
        if user:
            user_course = self._get_user_course(course_id, user.student.id)
            has_paid = user_course and user_course.has_paid
            if not has_paid:
                raise PermissionDenied

    def get_lesson_from_course(
            self,
            course_id: int,
            lessons_id: int,
    ) -> dict:
        lesson: Lesson = self.session.query(Lesson).join(Course).options(
            joinedload(Lesson.lesson_comment).options(joinedload(
                LessonComment.student
            ).options(joinedload(Student.user)))).options(
            joinedload(Lesson.photos)).options(
            joinedload(Lesson.videos)).filter(and_(
            Lesson.course_id == course_id, Lesson.id == lessons_id
        )).first()
        if not lesson:
            raise NotFound
        count_lessons = self.session.query(Lesson).filter(
            Lesson.course_id == course_id).count()
        lesson_teachers: Course = self.session.query(Course).options(
            joinedload(Course.teachers).options(
                joinedload(Teacher.user))).filter(
            and_(
                Course.id == course_id,
                Course.lessons.contains(lesson)
            )
        ).first()
        result_dict = {
            'lesson': lesson,
            'count_lessons': count_lessons,
            'lesson_teachers':
                [item.user.username for item in lesson_teachers.teachers]
        }
        self.__check_leesson_for_user(lesson, course_id)
        return result_dict

    def add_lesson_to_course(
            self,
            course_id: int,
            lesson_data: LessonBase,

    ) -> int:
        if self.is_teacher:
            teacher = self.user.teacher
            course: Course = self.get_current_item(course_id, Course).first()
            if teacher not in course.teachers:
                raise PermissionDenied
            if self.check_item_exists(course_id, Course):
                return self._create_lesson_instanse(course.id, lesson_data).id
        raise PermissionDenied

    def make_lessone_done(
            self,
            lessons_id: int,
    ) -> StudentPassedLesson | None:
        user = self.user
        if self.user and self.is_student:
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
        raise PermissionDenied

    def add_comment_to_lesson(
            self,
            text: CommentBase,
            lesson_id: int,
            course_id: int = None,
    ):
        """Добавить отзыв на урок."""
        if self.user and self.is_student:
            student = self.user.student
            new_comment = LessonComment(
                student_id=student.id,
                lesson_id=lesson_id,
                text=text.text
            )
            self.create_item(new_comment)
        raise PermissionDenied

    def remove_comment_from_lesson(
            self, comment_id: int, lesson_id: int,
    ):
        if self.is_student or self.is_staff:
            comment = self.session.query(LessonComment).filter(
                and_(
                    LessonComment.lesson_id == lesson_id,
                    LessonComment.id == comment_id
                )
            ).first()
            if not comment:
                raise NotFound
            self.remove_item(comment.id, LessonComment)
        raise PermissionDenied

    def remove_lesson(self, course_id: int, lesson_id: int):
        course: Course = self.get_current_item(course_id, Course).first()
        user = self.user
        if self.is_staff or (
                self.is_teacher and user.teacher in course.teachers
        ):
            self.remove_item(lesson_id, Lesson)
        raise PermissionDenied

    def add_lesson_in_favorite(self, lesson_id: int):
        if self.user and self.is_student:
            student = self.user.student
            lesson = self.get_current_item(lesson_id, Lesson).first()
            if lesson in student.favorite_lessons:
                raise NotFound
            student.favorite_lessons.append(lesson)
            self.session.commit()
            return self.get_json_reposnse('Урок добавлен в избранное', 201)
        raise PermissionDenied

    def remove_lesson_from_favorite(self, lesson_id: int):
        if self.user and self.is_student:
            student = self.user.student
            lesson = self.get_current_item(lesson_id, Lesson).first()
            if lesson not in student.favorite_lessons:
                raise NotFound
            student.favorite_lessons.remove(lesson)
            self.create_item(student)
            return self.get_json_reposnse('Урок удален из избранных', 201)
        raise PermissionDenied
