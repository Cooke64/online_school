from fastapi import APIRouter, Depends, Path, Body

from src.auth.utils.auth_bearer import JWTBearer, get_permission, \
    UserPermission, get_student_permission
from src.course.crud import CourseCrud
from src.course.shemas import CreateCourse, UpdateCourse, CourseListShow
from src.exceptions import NotFound, PermissionDenied
from src.users.models import RolesType

router = APIRouter(prefix='/course', tags=['Главная страничка курсов'])


@router.get('/', response_model=list[CourseListShow])
def get_all_courses(course_crud: CourseCrud = Depends()):
    return course_crud.get_all_items()


@router.get('/{course_id}')
def get_course_by_id(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends()
):
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound
    return query


@router.post('/add/{course_id}', dependencies=[Depends(JWTBearer())])
def add_course_in_users_list(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    """
    Добавляет пользователю выбранный курс
    param course_id: id курса
    param email: email пользователя
    """
    if not permission.role == RolesType.student.value:
        raise PermissionDenied
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound
    course_crud.add_course_by_user(course_id, permission.user_email)
    return {'course': 'added'}


@router.delete(
    '/remove/{course_id}',
    dependencies=[Depends(JWTBearer())],
    status_code=204,
    description='Удаление курса из списка курсов студента.'
)
def remove_course_from_users_list(
        course_id: int = Path(
            ...,
            description='id курса, который надо удалить'
        ),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    if not permission.role == RolesType.student.value:
        raise PermissionDenied
    course_crud.remove_course_from_list(
        course_id, permission.user_email
    )


@router.post('/', dependencies=[Depends(JWTBearer())])
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    if not permission.has_perm:
        raise PermissionDenied
    teacher = course_crud.get_teacher_by_email(permission.user_email)
    course_crud.create_new_course(course_data, teacher)
    return course_data


@router.put('/{course_id}', status_code=202,
            dependencies=[Depends(JWTBearer())])
def update_course(course_id: int,
                  course_data: UpdateCourse,
                  course_crud: CourseCrud = Depends(),
                  permission: UserPermission = Depends(get_permission)
                  ):
    # Проверка авторизации пользователя
    if not permission.has_perm:
        raise PermissionDenied
    course = course_crud.get_course_by_id(course_id)
    teacher = course_crud.get_teacher_by_email(permission.user_email)
    # Проверка, что учитель явлется одним из авторов курса
    if teacher not in course.teachers:
        raise PermissionDenied
    return course_crud.update_course(course_id, course_data)


@router.delete(
    '/{course_id}',
    status_code=204,
    dependencies=[Depends(JWTBearer())],
    description='Удаление курса по его id одним из создателей курса.'
)
def delete_course(
        course_id: int,
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission)
):
    if not permission.has_perm:
        raise PermissionDenied
    course = course_crud.get_course_by_id(course_id)
    teacher = course_crud.get_teacher_by_email(permission.user_email)
    if teacher not in course.teachers:
        raise PermissionDenied
    course_crud.delete_course(course_id)
