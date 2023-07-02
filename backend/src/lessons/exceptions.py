from src.exceptions import NotFound, PermissionDenied, BadRequest
from src.lessons.constants import ErrorCode


class NotFoundLesson(NotFound):
    DETAIL = ErrorCode.NOT_FOUND_LESSON


class HasNotPermission(PermissionDenied):
    DETAIL = ErrorCode.HAS_NOT_PERMISSON


class AddExisted(BadRequest):
    DETAIL = ErrorCode.ADD_EXISTED


class NotFoundObject(BadRequest):
    DETAIL = ErrorCode.NOT_FOUND_OBJECT


class NeedBuyCourse(BadRequest):
    DETAIL = ErrorCode.NEED_BUY_COURSE
