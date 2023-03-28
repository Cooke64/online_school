import time
import typing

from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from ...config import settings
from ...exceptions import NotAuthenticated
from ...users.crud import UserCrud
from ...users.models import RolesType


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
        is_valid = decoded_token['exp'] >= time.time()
        return decoded_token if is_valid else None
    except:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise NotAuthenticated
            if not self.verify_jwt(credentials.credentials):
                raise NotAuthenticated
            return credentials.credentials
        else:
            raise NotAuthenticated

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            return True
        return False


async def get_current_user(token: str = Depends(JWTBearer())) -> dict:
    payload = jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )
    return payload.get("sub")


class UserPermission(typing.NamedTuple):
    has_perm: bool
    role: str
    user_email: str


async def get_permission(
        email: str = Depends(get_current_user),
        user_crud: UserCrud = Depends()
) -> UserPermission:
    user = user_crud.get_user(email)
    if user and user.role in (RolesType.staff.value, RolesType.teacher.value):
        return UserPermission(True, user.role, email)
    return UserPermission(False, user.role)
