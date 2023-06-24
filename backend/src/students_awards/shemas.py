import datetime

from src.students_awards.models import AwardsTypes
from src.utils.base_schemas import OrmBaseModel


class AwardBase(OrmBaseModel):
    name: str


class AwardCreate(AwardBase):
    column_name: AwardsTypes
    amount_to_get: int

    class Config:
        schema_extra = {
            'example': {
                'name': 'Бог комментариев',
                'column_name': 'comments',
                'amount_to_get': 300
            }
        }


class ShowAwards(AwardBase):
    id: int


class ShowDetailAwards(OrmBaseModel):
    id: int
    when_get: datetime.datetime
    award: ShowAwards
