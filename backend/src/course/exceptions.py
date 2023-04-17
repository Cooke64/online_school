from src.course.constants import ErrorCode
from src.exceptions import NotFound, PermissionDenied, BadRequest


class NotFoundTeacher(NotFound):
    DETAIL = ErrorCode.NOT_FOUND_TEACHER


class NotFoundStudent(NotFound):
    DETAIL = ErrorCode.NOT_FOUND_STUDNET


class NotFoundCourse(NotFound):
    DETAIL = ErrorCode.NOT_FOUND_COURSE


class HasNotPermission(PermissionDenied):
    DETAIL = ErrorCode.HAS_NOT_PERMISSON


class AddExisted(BadRequest):
    DETAIL = ErrorCode.ADD_EXISTED
