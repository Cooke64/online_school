"""
This file is responsible for signing, creating or decode and returning JWTds.
"""
import json
from datetime import datetime, timedelta

import jwt

from src.config import settings

Token = dict[str]


def token_response(token: str) -> Token:
    """The function returns ready JWT token"""
    return {'access token': token}


def create_jwt(email: str, expires_delta: timedelta = None) -> token_response:
    """The function create JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    payload = {
        'email': email,
        'expiry': json.dumps(expire, default=str)
    }
    encoded_jwt = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def decode_jwt_token(token: str) -> str | None:
    """The function decode JWT token"""
    decode_token = jwt.decode(
        token, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return decode_token if decode_token['expires'] >= datetime.utcnow() else None

