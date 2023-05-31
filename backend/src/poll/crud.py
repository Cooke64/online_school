from sqlalchemy.orm import joinedload, Query

from src.database import BaseCrud
from .models import Poll, Question
from .schemas import PollBase, QuestionBase
from ..auth.utils.auth_bearer import UserPermission
from ..course.models import Course, Lesson
from ..exceptions import PermissionDenied, NotFound, BadRequest
from ..teachers.models import Teacher
from ..users.models import User


class PollCrud(BaseCrud):
    def get_teacher_by_email(self, email: str) -> Teacher:
        teacher = self.session.query(
            Teacher).join(User).filter(
            User.email == email).first()
        if not teacher:
            raise NotFound
        return teacher

    def _check_lesson_teacher(self, course_id: int | None = None, *, lesson_id,
                              permission: UserPermission) -> None:
        """
        Проверяет, что роль у авторизованного пользователя учитель.
        Далее идет проверка, что действительно есть такой урок,
        далее проверка, что данный пользователь является одним из преподавателей курса.
        Ничего не возвращает, при выполнении условия райзит ошибки.
        """
        lesson = self.get_current_item(lesson_id, Lesson).first()
        if not lesson:
            raise BadRequest
        if not course_id:
            course_id = lesson.course.id
        if not permission.role == 'Teacher':
            raise PermissionDenied
        teacher = self.get_teacher_by_email(permission.user_email)
        course: Course = self.get_current_item(course_id, Course).first()
        if teacher not in course.teachers:
            raise PermissionDenied

    def get_all_polls(self) -> list[Poll]:
        return self.session.query(Poll).options(
            joinedload(Poll.question_list)).all()

    def _get_current_poll(self, poll_id: int) -> Query:
        query = self.session.query(Poll).options(
            joinedload(Poll.question_list)).filter(Poll.id == poll_id)
        return query

    def _get_lesson_poll(self, lesson_id) -> Poll:
        query = self.session.query(Poll).options(
            joinedload(Poll.lesson)).filter(Poll.lesson_id == lesson_id)
        return query.first()

    def _create_poll(self, poll_data: PollBase, lesson_id: int) -> Poll:
        new_poll = Poll(lesson_id=lesson_id, **poll_data.dict())
        return self.create_item(new_poll)

    def add_poll_to_lesson(
            self, course_id: int, lesson_id: int,
            poll_data: PollBase,
            permission: UserPermission
    ) -> Poll:
        self._check_lesson_teacher(course_id=course_id, lesson_id=lesson_id, permission=permission)
        return self._create_poll(poll_data, lesson_id)

    def remove_poll(self, lesson_id: int, permission: UserPermission):
        self._check_lesson_teacher(lesson_id=lesson_id, permission=permission)
        lesson_poll = self._get_lesson_poll(lesson_id)
        self.remove_item(lesson_poll.id, Poll)
        return self.get_json_reposnse('Удален', 204)

    def _create_question(self, poll_id, question):
        new_question = Question(poll_id=poll_id, **question.dict())
        return self.create_item(new_question)

    def add_question(self, poll_id: int, question: QuestionBase,
                     permission: UserPermission):
        poll: Poll = self._get_current_poll(poll_id).first()
        self._check_lesson_teacher(lesson_id=poll.lesson_id,
                                   permission=permission)
        new_question = self._create_question(poll_id, question)
        poll.question_list.append(new_question)

    def remove_question(self, poll_id, question_id, permission):
        poll: Poll = self._get_current_poll(poll_id).first()
        self._check_lesson_teacher(lesson_id=poll.lesson_id,
                                   permission=permission)
        self.remove_item(question_id, Question)
        return self.get_json_reposnse('Удален', 204)
