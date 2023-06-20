from sqlalchemy import and_

import src.exceptions as ex
from src.students.crud import StudentCrud
from src.students_awards.models import AwardsTypes, Award
from src.students_awards.shemas import AwardCreate


class AwardCrud(StudentCrud):

    def _get_student_data(self) -> dict:
        """Считает статистику пользователя и возвращает словарь с результатами."""
        comments = self._get_student_comments()
        passed_lessons = self._get_student_passed_lesson()
        passed_by_day, *_ = self.get_lessons_passed_today()
        return {'comments': comments, 'passed_lessons': passed_lessons,
                'passed_by_day': passed_by_day}

    def __check_award(self, award_data: AwardCreate) -> bool:
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
        amount_difrent_awards = 3
        is_enought_awards = self.session.query(Award).filter(
            Award.name == award_data.name
        ).count() <= amount_difrent_awards
        return not same_award and is_enought_awards

    def create_new_awward(self, award_data: AwardCreate):
        # Проверка, что новая награда имеет column_name в списке доступных.
        if award_data.column_name not in [e.value for e in AwardsTypes]:
            raise ex.BadRequest
        if not self.__check_award(award_data):
            raise ex.BadRequest
        new_award = Award(**award_data.dict())
        return self.create_item(new_award)

    def get_student_award(self):
        ...
