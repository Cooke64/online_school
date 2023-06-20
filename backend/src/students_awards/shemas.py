from src.utils.base_schemas import OrmBaseModel


class AwardBase(OrmBaseModel):
    name: str
    column_name: str
    amount_to_get: int


class AwardCreate(AwardBase):
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
