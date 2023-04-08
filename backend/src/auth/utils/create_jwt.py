"""
This file is responsible for signing, creating or decode and returning JWTds.
"""
from datetime import datetime, timedelta

import jwt

from src.config import settings


def create_jwt(data: dict, expires_delta: timedelta | None = None):
    """The function create JWT token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=666)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY,
                             algorithm=settings.ALGORITHM)
    return encoded_jwt

