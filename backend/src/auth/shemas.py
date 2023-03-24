from uuid import UUID
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int = None


class Msg(BaseModel):
    msg: str


class VerificationCreate(BaseModel):

    user_id: int


class VerificationOut(BaseModel):
    link: UUID
