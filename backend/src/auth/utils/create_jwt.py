from datetime import datetime, timedelta

import jwt

from src.config import settings


def create_jwt_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        epxire_time = datetime.utcnow() + expires_delta
    else:
        epxire_time = datetime.utcnow() + timedelta(minutes=20)
    to_encode.update({'exp': epxire_time, 'sub': 'access'})
    encode_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                            algorithm=settings.ALGORITHM)
    return encode_jwt
