from fastapi import APIRouter, UploadFile, File, Depends, Path
from starlette.background import BackgroundTasks
from starlette.responses import FileResponse, StreamingResponse

from src.lesson_files.crud import MediaCrud
from src.lesson_files.schemas import LessonContentList
from src.lesson_files.utils.create_file import upload_file_and_push_to_db, \
    read_and_show_file, get_type_content

router = APIRouter(prefix='/lesson/content', tags=['Страница видео урок'])


@router.post('/post_video', )
async def upload_video(
        background_task: BackgroundTasks,
        video_file: UploadFile = File(...),
        media_crud: MediaCrud = Depends(),
):
    if video_file.content_type in ['video/mp4', 'video/quicktime']:
        background_task.add_task(
            upload_file_and_push_to_db, video_file, media_crud, is_photo=False)
    else:
        return media_crud.get_json_reposnse('Неправильный формат файла', 418)
    return media_crud.get_json_reposnse('Успешно загружен', 201)


@router.post('/post_photo')
async def upload_photo(
        background_task: BackgroundTasks,
        photos_list: list[UploadFile] = File(...),
        media_crud: MediaCrud = Depends(),
):
    for file in photos_list:
        if file.content_type in ['image/png', 'image/jpeg', 'image/jpg']:
            background_task.add_task(upload_file_and_push_to_db, file,
                                     media_crud)
            return media_crud.get_json_reposnse('Успешно загружен', 201)
        else:
            return media_crud.get_json_reposnse('Неправильный формат файла',
                                                418)


content = {
    'photos': [{'title': 'photo.1', 'description': 'description'},
               {'title': 'photo.2', 'description': 'description'}, ],
    'videos': [{'title': 'video.1', 'description': 'description'},
               {'title': 'video.2', 'description': 'description'}, ],
}


@router.get('/{lesson_id}', response_model=LessonContentList)
def get_lesson_content(lesson_id):
    return content


@router.get('/{lesson_id}/photos/')
def get_photo_from_lesson(
        lesson_id, media_crud: MediaCrud = Depends()
):
    file_list = media_crud.get_all_photos()

    def get_photo_iterator(files):
        for file in files:
            file_type = get_type_content(file.photo_type)
            file_path = read_and_show_file(file.photo_blob, file_type)
            with open(file_path, 'rb') as file_to_read:
                yield from file_to_read

    return StreamingResponse(get_photo_iterator(file_list),
                             media_type='image/png')


@router.get('/{lesson_id}/photo/{content_id}')
def get_photo_from_lesson(
        lesson_id,
        content_id: int = Path(...),
        media_crud: MediaCrud = Depends()):
    blob = media_crud.get_contnent(content_id)
    file_type = get_type_content(blob.photo_type)
    file_path = read_and_show_file(blob.photo_blob, file_type)
    return FileResponse(file_path)


@router.get('/{lesson_id}/video/{content_id}')
def get_video_from_lesson(
        lesson_id, content_id, media_crud: MediaCrud = Depends()):
    blob = media_crud.get_contnent(content_id, photo=False)
    file_type = get_type_content(blob.video_type)
    file_path = read_and_show_file(blob.video_blob, file_type)

    def iterfile(path_to_file):
        with open(path_to_file, 'rb') as file_to_read:
            yield from file_to_read

    return StreamingResponse(iterfile(file_path), media_type=blob.video_type)
