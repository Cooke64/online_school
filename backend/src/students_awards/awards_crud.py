import collections
import typing
from collections import OrderedDict
from typing import Any

from sqlalchemy import and_

import src.exceptions as ex
from src.students.crud import StudentCrud
from src.students_awards.models import AwardsTypes, Award, StudentAward
from src.students_awards.shemas import AwardCreate


class StudentData(typing.NamedTuple):
    cooments: int
    passed_lessons: int
    passed_by_day: int


Data = collections.namedtuple('StudentData',
                              ['cooments', 'passed_lessons', 'passed_by_day'])


class AwardCrud(StudentCrud):

    def __get_student_data(self) -> dict[str, Any] | OrderedDict[str, Any]:
        """Считает статистику пользователя и возвращает словарь с результатами."""
        comments = self._get_student_comments()
        passed_lessons = self._get_student_passed_lesson()
        passed_by_day, *_ = self.get_lessons_passed_today()
        return Data._make(
            (StudentData(comments, passed_lessons, passed_by_day)))._asdict()

    def __check_award(self,
                      award_data: AwardCreate,
                      amount_difrent_awards: int = 3
                      ) -> bool:
        """
        Проверяет, что наград с одним и тем же названием и количеством условных единиц еще не создано.
        Проверяет, что количество созданных наград не больше трех единиц.
        Возвращает True, если оба значение выполняются.
        """
        same_award = self.session.query(Award).filter(
            and_(
                Award.name == award_data.name,
                Award.amount_to_get == award_data.amount_to_get
            )
        ).first()
        is_enought_awards = self.session.query(Award).filter(
            Award.name == award_data.name
        ).count() <= amount_difrent_awards
        return not same_award and is_enought_awards

    def create_new_awward(self, award_data: AwardCreate) -> Award:
        # Проверка, что новая награда имеет column_name в списке доступных.
        if not self.is_teacher:
            if award_data.column_name not in [e.value for e in AwardsTypes]:
                raise ex.BadRequest
            if not self.__check_award(award_data):
                raise ex.BadRequest
            new_award = Award(**award_data.dict())
            return self.create_item(new_award)

    def __create_student_award(self, award_id: int):
        user = self.user
        new_student_award = StudentAward(
            student_id=user.student.id,
            award_id=award_id,

        )
        self.create_item(new_student_award)

    def get_student_award(self):
        awards_list: list[Award] = self.get_all_items(Award)
        for award in awards_list:
            for name, value in self.__get_student_data().items():
                if name == award.name and value:
                    self.__create_student_award(award.id)

    def get_all_awards(self) -> list[Award]:
        return self.get_all_items(Award)
