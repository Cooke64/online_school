from fastapi import APIRouter, Depends, Path, status, UploadFile, File
from starlette.background import BackgroundTasks

from src.auth.utils.auth_bearer import (
    JWTBearer,
    get_permission,
    UserPermission, get_teacher_permission
)
from src.course.crud import CourseCrud
from src.course.shemas import (
    CreateCourse,
    UpdateCourse,
    CourseListShow,
    CourseDetail, ReviewBase
)
from src.course.utils import Rating
from src.exceptions import NotFound, PermissionDenied
from src.lesson_files.crud import MediaCrud
from src.lesson_files.utils.create_file import upload_file_and_push_to_db, \
    create_preview_to_course
from src.users.models import RolesType
from src.utils.base_schemas import ErrorMessage

router = APIRouter(prefix='/course', tags=['Главная страничка курсов'])


def _check_params(course_id, permission, course_crud):
    if not permission.role == RolesType.student.value:
        raise PermissionDenied
    query = course_crud.get_course_by_id(course_id)
    if not query:
        raise NotFound


@router.get(
    '/',
    summary='Получить список всех курсов',
    response_model=list[CourseListShow]
)
def get_all_courses(course_crud: CourseCrud = Depends()):
    return course_crud.get_all_items()


@router.get(
    '/{course_id}',
    response_model=CourseDetail,
    responses={404: {"model": ErrorMessage}},
    summary='Получить курс по его id'
)
def get_course_by_id(
        course_id: int = Path(..., gt=0),
        course_crud: CourseCrud = Depends()
):
    return course_crud.get_course_by_id(course_id)


@router.post(
    '/{course_id}/add_rating',
    status_code=status.HTTP_201_CREATED,
    summary='Поставить оценку курсу. От 1 до 5'
)
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


@router.put('/{course_id}/update_rating', status_code=status.HTTP_201_CREATED,
            summary='Изменить рейтинг курса')
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
    return course_crud.get_json_reposnse('Рейтинг для курса изменен', 201)


@router.post('/add/{course_id}',
             dependencies=[Depends(JWTBearer())],
             status_code=status.HTTP_201_CREATED,
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
             status_code=status.HTTP_201_CREATED,
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
    return course_crud.pay_for_course(course_id, permission.user_email)


@router.delete(
    '/remove/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
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


@router.post('/', status_code=status.HTTP_201_CREATED,)
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends(),
        email: UserPermission = Depends(get_teacher_permission),
):
    return course_crud.create_new_course(course_data, email)


@router.put('/{course_id}',
            status_code=status.HTTP_202_ACCEPTED)
def update_course(course_id: int,
                  course_data: UpdateCourse,
                  course_crud: CourseCrud = Depends(),
                  permission: UserPermission = Depends(get_permission)
                  ):
    return course_crud.update_course(course_id, course_data, permission)


@router.delete(
    '/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Удаление курса по его id одним из создателей курса.'
)
def delete_course(
        course_id: int,
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission)
):
    """Удаление курса. Доступно авторизованному пользователю со статусом Учитель.
        - Учитель должен быть в списке учителей курса.
    """
    course_crud.delete_course(course_id, permission)


@router.post(
    '/{course_id}/add_review',
    status_code=status.HTTP_201_CREATED,
    description='Добавить отзыв курсу по его id.',
    summary='Добавить отзыв'
)
def add_review_to_course_by_student(
        review_data: ReviewBase,
        course_id: int = Path(..., gt=0),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    course_crud.add_review_to_course(course_id, permission.user_email, review_data)


@router.delete(
    '/{course_id}/delete_review/{review_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Удалить отзыв по id у курса по его id.',
    summary='Удалить отзыв'
)
def add_review_to_course_by_student(
        course_id: int = Path(..., gt=0),
        review_id: int = Path(..., gt=0),
        course_crud: CourseCrud = Depends(),
        permission: UserPermission = Depends(get_permission),
):
    course_crud.delete_review(permission.user_email, review_id, course_id)


@router.post(
    '/{course_id}/add_preview_photo',
    status_code=status.HTTP_201_CREATED,
    description='Добавить курсу фотографию на превью.',
    summary='Добавить превью'
)
def add_review_to_course_by_student(
        course_id: int,
        task: BackgroundTasks,
        photo: UploadFile = File(...),
        media_crud: MediaCrud = Depends(),
):
    task.add_task(
        create_preview_to_course,
        file_obj=photo,
        course_id=course_id,
    )
    return media_crud.get_json_reposnse('Успешно загружен', 201)
