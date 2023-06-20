from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound, PermissionDenied
from src.lessons.models import LessonComment
from src.lessons.shemas import LessonBase, CommentBase
from src.students.models import StudentCourse, StudentPassedLesson, Student
from src.teachers.models import Teacher
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
        result_dict = {'lesson': lesson,
                       'count_lessons': count_lessons,
                       'lesson_teachers':
                           [item.user.username for item in
                            lesson_teachers.teachers]
                       }
        if (lesson and lesson.is_trial) or self.is_teacher:
            return result_dict
        user = self.user
        if not user:
            raise PermissionDenied
        user_course = self._get_user_course(course_id, user.student.id)
        if user_course and user_course.has_paid:
            return result_dict
        raise PermissionDenied

    def add_lesson_to_course(
            self,
            course_id: int,
            lesson_data: LessonBase,

    ) -> int:
        user = self.user
        course: Course = self.get_current_item(course_id, Course).first()
        if user.teacher not in course.teachers:
            raise PermissionDenied
        if self.check_item_exists(course_id, Course):
            return self._create_lesson_instanse(course.id, lesson_data).id

    def make_lessone_done(
            self,
            lessons_id: int,
    ) -> StudentPassedLesson | None:
        user = self.user
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
            course_id: int = None,
    ):
        """Добавить отзыв на урок."""
        student = self.user.student
        new_comment = LessonComment(
            student_id=student.id,
            lesson_id=lesson_id,
            text=text.text
        )
        self.create_item(new_comment)

    def remove_comment_from_lesson(
            self, comment_id: int, lesson_id: int,
            ):
        student = self.user.student
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

    def remove_lesson(self, course_id: int, lesson_id: int):
        course: Course = self.get_current_item(course_id, Course).first()
        user = self.user
        if user.teacher not in course.teachers or not self.is_teacher:
            raise PermissionDenied
        self.remove_item(lesson_id, Lesson)
