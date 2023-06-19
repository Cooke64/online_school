from fastapi import APIRouter, Depends, Path, status, UploadFile, File
from starlette.background import BackgroundTasks

from src.auth.utils.auth_bearer import (
    JWTBearer,
)
from src.course.crud import CourseCrud
from src.course.shemas import (
    CreateCourse,
    UpdateCourse,
    CourseListShow,
    CourseDetail, ReviewBase
)
from src.course.utils import Rating
from src.lesson_files.utils.create_file import create_preview_to_course
from src.utils.base_schemas import ErrorMessage

router = APIRouter(prefix='/course', tags=['Главная страничка курсов'])


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
        *,
        # Enum class Rating
        rating: Rating
):
    """
    Доступно для зарегестрированного пользователя. Можно поставить только одну оценку.
    При простановке второй раз отметки, в бд изменяется оценка.
    """
    course_crud.add_rating_to_course(course_id, rating)
    return {'done': 'done'}


@router.post('/add/{course_id}',
             dependencies=[Depends(JWTBearer())],
             status_code=status.HTTP_201_CREATED,
             summary='Добавление курса в список курсов пользователя'
             )
def add_course_in_users_list(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
):
    """
    Добавляет пользователю выбранный курс. Доступно для зарегестрированного пользователя.
    """
    course_crud.add_course_by_user(course_id)
    return {'course': 'added'}


@router.post('/add/{course_id}/pay',
             status_code=status.HTTP_201_CREATED,
             summary='Оплата курса курса, который добавлен пользователем'
             )
def pay_for_course_in_user_list(
        course_id: int = Path(..., description='The id of current post'),
        course_crud: CourseCrud = Depends(),
):
    """
    Оплата курса. Доступно для зарегестрированного пользователя.
    Если курс платный, то он становится доступным пользователю.
    Логики оплаты иммитации оплаты нет. Изменяет поле в модели
    StudentCourse.has_payd на True default = False
    """
    return course_crud.pay_for_course(course_id)


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
):
    """
    Доступно для зарегестрированного пользователя.
    """
    course_crud.remove_course_from_list(course_id)


@router.post('/', status_code=status.HTTP_201_CREATED)
def create_course(
        course_data: CreateCourse,
        course_crud: CourseCrud = Depends(),
):
    return course_crud.create_new_course(course_data)


@router.put('/{course_id}',
            status_code=status.HTTP_202_ACCEPTED)
def update_course(course_id: int,
                  course_data: UpdateCourse,
                  course_crud: CourseCrud = Depends(),
                  ):
    return course_crud.update_course(course_id, course_data)


@router.delete(
    '/{course_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Удаление курса по его id одним из создателей курса.'
)
def delete_course(
        course_id: int,
        course_crud: CourseCrud = Depends(),
):
    """Удаление курса. Доступно авторизованному пользователю со статусом Учитель.
        - Учитель должен быть в списке учителей курса.
    """
    course_crud.delete_course(course_id)


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
):
    course_crud.add_review_to_course(course_id, review_data)


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
):
    course_crud.delete_review(review_id, course_id)


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
        course_crud: CourseCrud = Depends(),
):
    task.add_task(
        create_preview_to_course,
        file_obj=photo,
        course_id=course_id,
        course_crud=course_crud
    )
    return course_crud.get_json_reposnse('Успешно загружен', 201)
