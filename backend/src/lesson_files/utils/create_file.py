import os
import pathlib
import shutil

from fastapi import UploadFile

from src.lesson_files.crud import MediaCrud

BASE_DIRECTORY = pathlib.Path(__file__).absolute().parent


def upload_file_and_push_to_db(
        file_obj: UploadFile,
        media_crud: MediaCrud,
        is_photo: bool = True,
        folder_name: str | None = None) -> None:
    DIR = f'{BASE_DIRECTORY}/{folder_name}/' if folder_name else BASE_DIRECTORY
    with open(f'{DIR}/{file_obj.filename}', 'wb') as buffer:
        shutil.copyfileobj(file_obj.file, buffer)
    with open(f'{DIR}/{file_obj.filename}', 'rb') as file:
        data_to_save = file.read()
        media_crud.upload_content(
            blob=data_to_save, file_type=file_obj.content_type,
            photo_content=is_photo)
    os.remove(f'{DIR}/{file_obj.filename}')


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
