from fastapi import APIRouter, Depends, Path

from src.auth.utils.auth_bearer import JWTBearer, get_permission, \
    UserPermission
from src.course.crud import CourseCrud
from src.course.shemas import CreateCourse, UpdateCourse, CourseListShow
from src.course.utils import Rating
from src.exceptions import NotFound, PermissionDenied
from src.users.models import RolesType

router = APIRouter(prefix='/course', tags=['Главная страничка курсов'])


def _check_params(course_id, permission, course_crud):
    if not permission.role == RolesType.student.value:
        raise PermissionDenied
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound


@router.get(
    '/',
    response_model=list[CourseListShow],
    summary='Получить список всех курсов'
)
def get_all_courses(course_crud: CourseCrud = Depends()):
    return course_crud.get_all_items()


@router.get('/{course_id}', summary='Получить курсов по его id')
def get_course_by_id(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends()
):
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound
    return query


@router.post('/{course_id}/add_rating', status_code=201, summary='Поставить оценку курсу. От 1 до 5')
def add_rating_to_course(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
        *,
        rating: Rating
):
    """
    Доступно для зарегестрированного пользователя. Можно поставить только одну оценку.
    """
    _check_params(course_id, permission, course_crud)
    course_crud.add_rating_to_course(permission.user_email, course_id, rating)
    return {'done': 'done'}


@router.put('/{course_id}/update_rating', status_code=201, summary='Изменить рейтинг курса')
def update_rating_to_course(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
        *,
        new_rating: Rating
):
    """
    Доступно для зарегестрированного пользователя.
    """
    _check_params(course_id, permission, course_crud)
    course_crud.update_rating(permission.user_email, course_id, new_rating)
    return {'done': 'done'}


@router.post('/add/{course_id}',
             dependencies=[Depends(JWTBearer())],
             status_code=201,
             summary='Добавление курса в список курсов пользователя'
             )
def add_course_in_users_list(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    """
    Добавляет пользователю выбранный курс. Доступно для зарегестрированного пользователя.
    """
    _check_params(course_id, permission, course_crud)
    course_crud.add_course_by_user(course_id, permission.user_email)
    return {'course': 'added'}


@router.post('/add/{course_id}/pay',
             dependencies=[Depends(JWTBearer())],
             status_code=201,
             summary='Оплата курса курса, который добавлен пользователем'
             )
def pay_for_course_in_user_list(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    """
    Оплата курса. Доступно для зарегестрированного пользователя.
    Если курс платный, то он становится доступным пользователю.
    Логики оплаты иммитации оплаты нет. Изменяет поле в модели
    StudentCourse.has_payd на True default = False
    """
    _check_params(course_id, permission, course_crud)
    course_crud.pay_for_course(course_id, permission.user_email)


@router.delete(
    '/remove/{course_id}',
    dependencies=[Depends(JWTBearer())],
    status_code=204,
    summary='Удаление курса из списка курсов студента.'
)
def remove_course_from_users_list(
        course_id: int = Path(
            ...,
            description='id курса, который надо удалить'
        ),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    """
    Доступно для зарегестрированного пользователя.
    """
    if not permission.role == RolesType.student.value:
        raise PermissionDenied
    course_crud.remove_course_from_list(
        course_id, permission.user_email
    )


@router.post('/', dependencies=[Depends(JWTBearer())], status_code=201)
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    if not permission.has_perm or permission.role == RolesType.teacher.value:
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
