from fastapi import APIRouter

router = APIRouter(prefix='/user', tags=['Пользователи'])


@router.get('/')
def get_user_page():
    return {"access_token": 123, "token_type": "bearer"}
