from pydantic import BaseModel


class UploadVideo(BaseModel):
    title: str
    description: str


class PhotoItem(UploadVideo):
    pass


class VideoItem(UploadVideo):
    pass


class LessonContentList(BaseModel):
    photos: list[PhotoItem] | None
    videos: list[VideoItem] | None
