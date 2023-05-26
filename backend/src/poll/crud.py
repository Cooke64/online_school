from sqlalchemy.orm import joinedload, Query

from src.database import BaseCrud
from .models import Poll
from .schemas import PollBase
from ..auth.utils.auth_bearer import UserPermission
from ..course.models import Course
from ..exceptions import BadRequest, PermissionDenied, NotFound
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

    def _check_lesson_teacher(self, lesson_id, permission: UserPermission):
        if not permission.role == 'Teacher':
            raise PermissionDenied
        teacher = self.get_teacher_by_email(permission.user_email)
        lesson = self._get_lesson_poll(lesson_id)
        if lesson:
            raise BadRequest
        course = self.session.query(Course).filter(
            Course.lessons.contains(lesson)).first()
        if teacher not in course.teachers:
            raise PermissionDenied

    def get_all_polls(self) -> list[Poll]:
        return self.session.query(Poll).all()

    def _get_current_poll(self, poll_id: int) -> Query:
        query = self.session.query(Poll).options(
            joinedload(Poll.question_list)).filter(Poll.id == poll_id)
        return query

    def _get_lesson_poll(self, lesson_id):
        query = self.session.query(Poll).options(
            joinedload(Poll.lesson)).filter(Poll.lesson_id == lesson_id)
        return query.first()

    def _create_poll(self, poll_data: PollBase, lesson_id: int) -> Poll:
        new_poll = Poll(lesson_id=lesson_id, **poll_data.dict())
        return self.create_item(new_poll)

    def add_poll_to_lesson(
            self, lesson_id: int,
            poll_data: PollBase,
            permission: UserPermission
    ) -> Poll:
        self._check_lesson_teacher(lesson_id, permission)
        return self._create_poll(poll_data, lesson_id)

    def remove_poll(self, lesson_id: int, permission: UserPermission):
        self._check_lesson_teacher(lesson_id, permission)
        lesson_poll = self._get_lesson_poll(lesson_id)
        self.remove_item(lesson_poll.id, Poll)
