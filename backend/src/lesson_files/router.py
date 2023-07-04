import base64

from fastapi import APIRouter, UploadFile, File, Depends, Path
from starlette import status
from starlette.background import BackgroundTasks
from starlette.responses import StreamingResponse
from src.lesson_files.constants import ErrorCode as ex
from src.lesson_files.crud import MediaCrud
from src.lesson_files.utils.create_file import (
    upload_file_and_push_to_db,
    read_and_show_file,
    get_type_content
)

router = APIRouter(prefix='/lesson_content', tags=['Страница видео урок'])
VIDEO_TYPES = ('video/mp4', 'video/quicktime')
PHOTO_TYPES = ('image/png', 'image/jpeg', 'image/jpg')


@router.post(
    '/{lesson_id}/upload_video',
    summary='Загрузка видео для урока',
    status_code=201)
async def upload_video_to_lesson(
        lesson_id: int,
        task: BackgroundTasks,
        video_file: UploadFile = File(...),
        media_crud: MediaCrud = Depends(),
):
    """
        Реализует функцию загрузки видео с привязкой к уроку.
        Загрузка видео в бд осуществляется в асинхронном режиме
        с исспользованием BackgroundTasks.
        Допускается загружать только установленные форматы видеофайлов,
        указанных в кортеже VIDEO_TYPES. Допускается загрузить только одно видео к уроку
    """
    check = media_crud.check_lesson_teacher(lesson_id)
    if check:
        return check
    if video_file.content_type in VIDEO_TYPES:
        task.add_task(
            upload_file_and_push_to_db,
            file_obj=video_file,
            media_crud=media_crud,
            lesson_id=lesson_id,
            is_photo=False
        )
        return media_crud.get_json_reposnse(*ex.CREATED)
    else:
        return media_crud.get_json_reposnse(*ex.WRONG_TYPE)


@router.post(
    '/{lesson_id}/upload_photo',
    status_code=201,
    summary='Загрузка фотографий для урока'
)
async def upload_photo_to_lesson(
        lesson_id: int,
        task: BackgroundTasks,
        photo: UploadFile = File(...),
        media_crud: MediaCrud = Depends(),
):
    """
        Реализует функцию загрузки фотографии с привязкой к уроку.
        Загрузка фотографии в бд осуществляется в асинхронном режиме
        с исспользованием BackgroundTasks.
        Допускается загружать только установленные форматы фото, указанных в кортеже PHOTO_TYPES.
        Допускается загрузить неограниченное количество фотографий
    """
    check = media_crud.check_lesson_teacher(lesson_id)
    if check:
        return check
    if photo.content_type in PHOTO_TYPES:
        task.add_task(
            upload_file_and_push_to_db,
            file_obj=photo,
            media_crud=media_crud,
            lesson_id=lesson_id
        )
        return media_crud.get_json_reposnse(*ex.CREATED)
    else:
        return media_crud.get_json_reposnse(*ex.WRONG_TYPE)


@router.get('/{lesson_id}/photo/{photo_id}')
def get_photo_from_lesson(
        lesson_id: int = Path(...),
        photo_id: int = Path(...),
        media_crud: MediaCrud = Depends()):
    blob = media_crud.get_photo_item(photo_id, lesson_id)
    file_type = get_type_content(blob.photo_type)
    file_path = read_and_show_file(blob.photo_blob, file_type)
    with open(file_path, 'rb') as f:
        base64image = base64.b64encode(f.read())
    return base64image


@router.delete(
    '/{lesson_id}/photo/{photo_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Удалить фото в  уроке по его id.',
    summary='Удалить фото'
)
def remove_photo(
        lesson_id: int = Path(..., gt=0),
        photo_id: int = Path(..., gt=0),
        media_crud: MediaCrud = Depends(),
):
    check = media_crud.check_lesson_teacher(lesson_id)
    if check:
        return check
    media_crud.remove_photo(lesson_id, photo_id)
    return media_crud.get_json_reposnse(*ex.DELETED)


@router.get('/{lesson_id}/video/{video_id}')
def get_video_from_lesson(
        lesson_id, video_id, media_crud: MediaCrud = Depends()):
    blob = media_crud.get_viedo_item(lesson_id, video_id)
    file_type = get_type_content(blob.video_type)
    file_path = read_and_show_file(blob.video_blob, file_type)

    def iterfile(path_to_file):
        with open(path_to_file, 'rb') as file_to_read:
            yield from file_to_read

    return StreamingResponse(iterfile(file_path), media_type=blob.video_type)
