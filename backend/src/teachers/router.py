from enum import Enum

from fastapi import APIRouter, Body, Depends, Path, UploadFile, File
from starlette.background import BackgroundTasks
from starlette.responses import RedirectResponse

from .crud import TeachersCrud
from .shemas import ShowTeachersList
from ..auth.utils.auth_bearer import get_current_user, \
    get_permission, UserPermission
from ..auth.utils.create_jwt import create_jwt
from ..auth.utils.hasher import verify_password
from ..exceptions import NotFound, BadRequest
from ..lesson_files.utils.create_file import upload_user_pic


router = APIRouter(prefix='/teachers', tags=['Преподаватели'])


@router.get('/', response_model=list[ShowTeachersList])
def get_teacher_list(
        teachers_crud: TeachersCrud = Depends(),
):
    return teachers_crud.get_teachers_data()
