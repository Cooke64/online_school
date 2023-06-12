from src.exceptions import BadRequest


class AddExisted(BadRequest):
    DETAIL = 'У данного урока уже есть опрос'
