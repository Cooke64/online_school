from sqlalchemy.orm import joinedload

from src.database import BaseCrud
from .models import Poll, Question


class PollCrud(BaseCrud):
    def get_all_polls(self) -> list[Poll]:
        return self.session.query(Poll).join(Question).all()

    def _get_current_poll(self, poll_id: int) -> Poll:
        query = self.session.query(Poll).options(
            joinedload(Poll.question_list)).filter(Poll.id == poll_id).first()
        return query
