from fastapi import APIRouter, Depends

from src.course.crud import CourseCrud

router = APIRouter(prefix='/student', tags=['Данные о студенте'])

#
# @router.get('/me')
# def get_all_courses():
#     pass
