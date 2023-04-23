import base64
import os
import pathlib
import shutil

from fastapi import UploadFile, Depends

from src.course.crud import CourseCrud
from src.lesson_files.crud import MediaCrud

BASE_DIRECTORY = pathlib.Path(__file__).absolute().parent


def create_blob_obj(file_obj):
    with open(f'{BASE_DIRECTORY}/{file_obj.filename}', 'wb') as buffer:
        shutil.copyfileobj(file_obj.file, buffer)
    with open(f'{BASE_DIRECTORY}/{file_obj.filename}', 'rb') as file:
        return base64.b64encode(file.read())


def upload_file_and_push_to_db(
        file_obj: UploadFile,
        media_crud: MediaCrud,
        lesson_id: int,
        is_photo: bool = True,
) -> None:
    data_to_save = create_blob_obj(file_obj)
    media_crud.upload_content(
        blob=data_to_save,
        file_type=file_obj.content_type,
        lesson_id=lesson_id,
        photo_content=is_photo)
    os.remove(f'{BASE_DIRECTORY}/{file_obj.filename}')


def create_preview_to_course(file_obj: UploadFile, course_id: int, course_crud: CourseCrud = Depends()):
    data_to_save = create_blob_obj(file_obj)
    file_type = get_type_content(file_obj.content_type)
    file_path = read_and_show_file(data_to_save, file_type)
    with open(file_path, 'rb') as f:
        base64image = base64.b64encode(f.read())
    course_crud.add_preview(
        course_id, base64image, file_obj.content_type
    )
    os.remove(f'{BASE_DIRECTORY}/{file_obj.filename}')


def get_type_content(file_type: str):
    if file_type == 'video/quicktime':
        return 'mov'
    return file_type.split('/')[1]


def read_and_show_file(
        blob_file: bytes,
        file_type: str = 'png',
        folder_name: str | None = None):
    DIR = f'{BASE_DIRECTORY}/{folder_name}/' if folder_name else BASE_DIRECTORY
    with open(f'{DIR}/temp.{file_type}', 'wb') as file:
        file.write(blob_file)
    return f'{DIR}/temp.{file_type}'
