from pydantic import BaseModel

from src.utils.base_schemas import OrmBaseModel


class LessonVideo(OrmBaseModel):
    id: int


class LessonPhoto(OrmBaseModel):
    id: int


class LessonContentList(OrmBaseModel):
    photos: list[LessonVideo] | None
    videos: list[LessonPhoto] | None
