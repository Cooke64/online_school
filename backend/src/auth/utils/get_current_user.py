from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError

from src.auth.utils.auth_bearer import decode_jwt
from src.exceptions import NotAuthenticated
from src.users.crud import UserCrud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login", scheme_name="JWT")


async def get_email_by_token(
        token: Annotated[str, Depends(oauth2_scheme)],
        course_crud: UserCrud = Depends()
):
    try:
        payload = decode_jwt(token)
        email: str = payload.get("sub")
        if not email:
            raise NotAuthenticated
    except JWTError:
        raise NotAuthenticated
    user = course_crud.get_user(email)
    if not user:
        raise NotAuthenticated
    return user

