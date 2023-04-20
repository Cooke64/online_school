import base64

from fastapi import APIRouter, UploadFile, File, Depends, Path
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse, StreamingResponse

from src.exceptions import DetailedHTTPException
from src.lesson_files.crud import MediaCrud
from src.lesson_files.schemas import LessonContentList
from src.lesson_files.utils.create_file import (
    upload_file_and_push_to_db,
    read_and_show_file,
    get_type_content
)

router = APIRouter(prefix='/lesson/content', tags=['Страница видео урок'])
VIDEO_TYPES = ('video/mp4', 'video/quicktime')
PHOTO_TYPES = ('image/png', 'image/jpeg', 'image/jpg')


@router.get('/{lesson_id}/', response_model=LessonContentList)
def get_lesson_content(
        lesson_id: int,
        media_crud: MediaCrud = Depends(),
):
    return media_crud.get_lesson_content(lesson_id)


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
    if video_file.content_type in VIDEO_TYPES:
        try:
            task.add_task(
                upload_file_and_push_to_db,
                file_obj=video_file,
                media_crud=media_crud,
                lesson_id=lesson_id,
                is_photo=False
            )
            return media_crud.get_json_reposnse('Успешно загружен', 201)
        except:
            raise DetailedHTTPException
    else:
        return media_crud.get_json_reposnse('Неправильный формат файла', 418)


@router.post(
    '/{lesson_id}/upload_photo',
    status_code=201,
    summary='Загрузка фотографий для урока'
)
async def upload_photo_to_lesson(
        lesson_id: int,
        task: BackgroundTasks,
        photos_list: list[UploadFile] = File(...),
        media_crud: MediaCrud = Depends(),
):
    """
        Реализует функцию загрузки фотографии с привязкой к уроку.
        Загрузка фотографии в бд осуществляется в асинхронном режиме
        с исспользованием BackgroundTasks.
        Допускается загружать только установленные форматы фото, указанных в кортеже PHOTO_TYPES.
        Допускается загрузить неограниченное количество фотографий
    """
    for file in photos_list:
        if file.content_type in PHOTO_TYPES:
            task.add_task(
                upload_file_and_push_to_db,
                file_obj=file,
                media_crud=media_crud,
                lesson_id=lesson_id
            )
            return media_crud.get_json_reposnse('Успешно загружен', 201)
        else:
            return media_crud.get_json_reposnse(
                'Неправильный формат файла', 418)


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
