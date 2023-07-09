from sqlalchemy import and_, func
from sqlalchemy.orm import joinedload

from src.course.models import Course, Lesson
from src.main_crud import BaseCrud
from src.lessons import exceptions as ex
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
        raise ex.NotFoundObject

    def __check_leesson_for_user(self, lesson: Lesson, course_id: int) -> None:
        user_type = self.is_teacher or self.is_staff
        is_trial = lesson and lesson.is_trial or user_type
        if not is_trial:
            raise ex.NeedBuyCourse
        user = self.user
        if user and self.is_student:
            user_course = self._get_user_course(course_id, user.student.id)
            has_paid = user_course and user_course.has_paid
            if not lesson.is_trial and not has_paid:
                raise ex.NeedBuyCourse
            return
        raise ex.HasNotPermission

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
            raise ex.NotFoundObject
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
        teacher = self.teacher
        course: Course = self.get_current_item(course_id, Course).first()
        if teacher not in course.teachers:
            raise ex.PermissionDenied
        if self.check_item_exists(course_id, Course):
            return self._create_lesson_instanse(course.id, lesson_data).id

    def make_lessone_done(
            self,
            lessons_id: int,
    ) -> StudentPassedLesson | None:
        """Длеает пометку в бд, что студент прошел урок при условии:
            - Курс должен быть куплен или урок должен быть бесплатным
            - Делает только одну уникальную пометку, что урок пройден или генерит ошибку
            - Подставляет дату, когда был пройден урок - текущее время и дата
        """
        student = self.student
        course = self.session.query(Course).join(Lesson).filter(
            Lesson.id == lessons_id
        ).first()
        lesson = self.get_current_item(lessons_id, Lesson).first()
        has_paid = self.session.query(StudentCourse).filter(
            StudentCourse.course_id == course.id,
            StudentCourse.student_id == student.id
        ).first()
        if lesson.is_trial or (has_paid and has_paid.has_paid):
            passed_lesson: StudentPassedLesson = self.session.query(
                StudentPassedLesson).filter(
                StudentPassedLesson.student_id == student.id,
                StudentPassedLesson.lesson_id == lessons_id,
            ).first()
            if not passed_lesson:
                passed_lesson.when_pass = func.now()
                passed_lesson.has_pass = True
                self.session.commit()
                return passed_lesson
            raise ex.NeedBuyCourse
        raise ex.PermissionDenied

    def add_comment_to_lesson(
            self,
            text: CommentBase,
            lesson_id: int,
            course_id: int = None,
    ):
        """Добавить отзыв на урок."""
        if self.student:
            new_comment = LessonComment(
                student_id=self.student.id,
                lesson_id=lesson_id,
                text=text.text
            )
            self.create_item(new_comment)
        raise ex.HasNotPermission

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
                raise ex.NotFoundObject
            self.remove_item(comment.id, LessonComment)
        raise ex.HasNotPermission

    def remove_lesson(self, course_id: int, lesson_id: int):
        """Удалить курс может авор курса или модератор."""
        is_teacher = self.session.query(Course).filter(
            and_(
                Course.id == course_id,
                Course.teachers.contains(self.user.teacher)
            )).first()
        if self.is_staff or is_teacher:
            self.remove_item(lesson_id, Lesson)
            return self.get_json_reposnse('Урок удален', 204)
        raise ex.HasNotPermission

    def add_lesson_in_favorite(self, lesson_id: int):
        student = self.student
        lesson = self.get_current_item(lesson_id, Lesson).first()
        if lesson not in student.favorite_lessons:
            student.favorite_lessons.append(lesson)
            self.session.commit()
            return self.get_json_reposnse('Урок добавлен в избранное', 201)
        return self.get_json_reposnse('Урок уже был добавлен в избранное', 400)

    def remove_lesson_from_favorite(self, lesson_id: int):
        student = self.student
        lesson = self.get_current_item(lesson_id, Lesson).first()
        if lesson not in student.favorite_lessons:
            raise ex.NotFoundObject
        student.favorite_lessons.remove(lesson)
        self.create_item(student)
        return self.get_json_reposnse('Урок удален из избранных', 201)
