import time

from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

from ...config import settings
from ...exceptions import NotAuthenticated


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
        isTokenValid: bool = False
        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            isTokenValid = True
        return isTokenValid


async def get_current_user(token: str = Depends(JWTBearer())) -> dict:
    # skipping verify since its already verified in JWTBearer
    payload = jwt.decode(
        token=token,
        key=settings.SECRET_KEY,
        algorithms=settings.ALGORITHM
    )
    return payload.get("sub")