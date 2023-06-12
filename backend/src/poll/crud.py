from sqlalchemy import exists
from sqlalchemy.orm import Query
from sqlalchemy.orm import joinedload

from src.database import BaseCrud
from .excteptions import AddExisted
from .models import Poll, Question, Answer
from .schemas import PollBase, QuestionBase, AnswerBase, AddAnswers
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
        if not self.session.query(
                exists().where(Poll.lesson_id == lesson_id)).scalar():
            new_poll = Poll(lesson_id=lesson_id, **poll_data.dict())
            return self.create_item(new_poll)
        raise AddExisted

    def add_poll_to_lesson(
            self, course_id: int, lesson_id: int,
            poll_data: PollBase,
            permission: UserPermission
    ) -> Poll:
        self._check_lesson_teacher(course_id=course_id, lesson_id=lesson_id,
                                   permission=permission)
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
        return self.get_json_reposnse(f'Вопрос добавленс номером {new_question.id}', 201)

    def remove_question(self, poll_id, question_id,
                        permission: UserPermission):
        poll: Poll = self._get_current_poll(poll_id).first()
        self._check_lesson_teacher(lesson_id=poll.lesson_id,
                                   permission=permission)
        self.remove_item(question_id, Question)
        return self.get_json_reposnse('Удален', 204)

    def _create_answer_instanse(self, question_id: int,
                                answer_data: AnswerBase) -> Answer:
        """Создает новый объект в модели Answer"""
        new_answer = Answer(question_id=question_id, **answer_data.dict())
        return self.create_item(new_answer)

    def add_answers_list(self, poll_id: int, question_id: int,
                         answeers_list: AddAnswers,
                         permission: UserPermission):
        """Получает список всех ответов к вопросу, при иттерации создается
        новая сущность модели ANswer, добавляется в
        answers_list - список ответовов к вопросу """
        poll: Poll = self._get_current_poll(poll_id).first()
        self._check_lesson_teacher(lesson_id=poll.lesson_id,
                                   permission=permission)
        question = self.get_current_item(question_id, Question).first()
        if question:
            for answer in answeers_list.answers_list:
                new_answer = self._create_answer_instanse(question_id, answer)
                question.answers_list.append(new_answer)
            return self.get_json_reposnse('Добавлено', 201)

    def get_lesson_poll(self, lesson_id):
        query: Poll = self.session.query(Poll).options(
            joinedload(Poll.question_list).options(
                joinedload(Question.answers_list))).filter(
            Poll.lesson_id == lesson_id
        ).first()
        if query:
            return query
        return NotFound
