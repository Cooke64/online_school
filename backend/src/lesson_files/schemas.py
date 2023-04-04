from pydantic import BaseModel


class LessonVideo(BaseModel):
    id: int

    class Config:
        orm_mode = True


class LessonPhoto(BaseModel):
    id: int

    class Config:
        orm_mode = True


class LessonContentList(BaseModel):
    photos: list[LessonVideo] | None
    videos: list[LessonPhoto] | None

    class Config:
        orm_mode = True
