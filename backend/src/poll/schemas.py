from pydantic import BaseModel, EmailStr, Field, constr, validator

from src.utils.base_schemas import OrmBaseModel


class PollBase(BaseModel):
    title: str

