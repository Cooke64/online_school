from sqlalchemy.orm import Query
from sqlalchemy.orm import joinedload

from src.database import BaseCrud
from .models import Poll, Question, Answer
from .schemas import PollBase, QuestionBase, AnswerBase, AddAnswers, AddPoll
from ..course.models import Course, Lesson
from ..exceptions import PermissionDenied, NotFound


class PollCrud(BaseCrud):

    def _check_lesson_teacher(self, course_id: int | None = None, *,
                              lesson_id) -> None:
        """
        Проверяет, что роль у авторизованного пользователя учитель.
        Далее идет проверка, что действительно есть такой урок,
        далее проверка, что данный пользователь является одним из преподавателей курса.
        Ничего не возвращает, при выполнении условия райзит ошибки.
        """
        lesson = self.get_current_item(lesson_id, Lesson).first()
        if not course_id:
            course_id = lesson.course.id
        teacher = self.teacher
        course: Course = self.get_current_item(course_id, Course).first()
        if teacher not in course.teachers or not self.is_staff:
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
        """Создает новый опрос или возвращает имеющийся в бд объект модели"""
        poll = self.session.query(Poll).filter(
            Poll.lesson_id == lesson_id).first()
        if not poll:
            new_poll = Poll(lesson_id=lesson_id, **poll_data.dict())
            return self.create_item(new_poll)
        return poll

    def add_poll_to_lesson(
            self, course_id: int, lesson_id: int,
            poll_data: PollBase,
    ) -> Poll:
        """Добавление опроса к уроку. Опрос должен быть уникальным. При попытке создать второй
        опрос к уроку возвращает id записи существующего опроса.
        """
        self._check_lesson_teacher(course_id=course_id, lesson_id=lesson_id)
        return self._create_poll(poll_data, lesson_id)

    def remove_poll(self, lesson_id: int):
        self._check_lesson_teacher(lesson_id=lesson_id)
        lesson_poll = self._get_lesson_poll(lesson_id)
        self.remove_item(lesson_poll.id, Poll)
        return self.get_json_reposnse('Удален', 204)

    def _create_question_instanse(
            self, poll_id: int, question: QuestionBase) -> Question:
        new_question = Question(poll_id=poll_id, **question.dict())
        return self.create_item(new_question)

    def add_question(self, poll_id: int, question: QuestionBase) -> Question:
        """
        Добавляет вопрос к опросу. Создает новую запись в бд, может
        быть неограниченное колличество вопросов в опросе. Список ответов может быть пустым.
        Может быть указано количество правильных ответов в вопросе. Дефолтное значение 0.
        """
        if self.is_teacher:
            poll: Poll = self._get_current_poll(poll_id).first()
            self._check_lesson_teacher(lesson_id=poll.lesson_id)
            new_question = self._create_question_instanse(poll_id, question)
            poll.question_list.append(new_question)
            return new_question
        raise PermissionDenied

    def remove_question(self, poll_id, question_id):
        poll: Poll = self._get_current_poll(poll_id).first()
        self._check_lesson_teacher(lesson_id=poll.lesson_id)
        self.remove_item(question_id, Question)
        return self.get_json_reposnse('Удален', 204)

    def _create_answer_instanse(self, question_id: int,
                                answer_data: AnswerBase) -> Answer:
        """Создает новый объект в модели Answer"""
        new_answer = Answer(question_id=question_id, **answer_data.dict())
        return self.create_item(new_answer)

    def add_answers_list(self, poll_id: int, question_id: int,
                         answeers_list: AddAnswers):
        """Получает список всех ответов к вопросу, при иттерации создается
        новая сущность модели ANswer, добавляется в
        answers_list - список ответовов к вопросу """
        if self.is_teacher:
            poll: Poll = self._get_current_poll(poll_id).first()
            self._check_lesson_teacher(lesson_id=poll.lesson_id)
            question = self.get_current_item(question_id, Question).first()
            if question:
                is_list = answeers_list.answers_list
                for answer in is_list if is_list else answeers_list:
                    new_answer = self._create_answer_instanse(question_id, answer)
                    question.answers_list.append(new_answer)
                return self.get_json_reposnse('Добавлено', 201)
        raise PermissionDenied

    def get_lesson_poll(self, lesson_id):
        query: Poll = self.session.query(Poll).options(
            joinedload(Poll.question_list).options(
                joinedload(Question.answers_list))).filter(
            Poll.lesson_id == lesson_id
        ).first()
        if query:
            return query
        return NotFound

    def add_new_poll(self,
                     course_id: int, lesson_id: int,
                     poll_data: AddPoll):
        poll_desc = PollBase(poll_description=poll_data.poll_description)
        poll = self.add_poll_to_lesson(
            course_id, lesson_id, poll_desc)
        poll_id = poll if isinstance(poll, int) else poll.id
        question = self.add_question(
            poll_id,
            poll_data.question,
        )
        self.add_answers_list(poll_id, question.id, poll_data.answers)
