from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from src.course.models import Lesson
from src.database import BaseCrud
from src.exceptions import NotFound
from src.lesson_files.models import LessonPhoto, LessonVideo


class MediaCrud(BaseCrud):

    def get_lesson_content(self, lesson_id):
        result: Lesson = self.session.query(Lesson).options(
            joinedload(Lesson.photos)).options(
            joinedload(Lesson.videos)).filter(
            Lesson.id == lesson_id
        ).first()
        return result

    def upload_content(
            self,
            blob: bytes,
            file_type: str,
            lesson_id: int,
            photo_content: bool = True
    ):
        lesson = self.get_current_item(lesson_id, Lesson).first()
        if photo_content:
            lesson_photo = LessonPhoto(
                photo_blob=blob,
                photo_type=file_type,
                lesson_content_id=lesson.id
            )
            self.create_item(lesson_photo)
        else:
            lesson_photo = LessonVideo(
                video_blob=blob,
                lesson_content_id=lesson.id,
                video_type=file_type,
            )
            self.create_item(lesson_photo)

    def get_photo_item(self, photo_id, lesson_id) -> LessonPhoto:
        query = self.session.query(LessonPhoto).join(Lesson).filter(
            and_(
                Lesson.id == lesson_id, LessonPhoto.id == photo_id
            )
        ).first()
        if not query:
            raise NotFound
        return query

    def get_viedo_item(self, video_id, lesson_id) -> LessonVideo:
        query = self.session.query(LessonVideo).join(Lesson).filter(
            and_(
                Lesson.id == lesson_id, LessonVideo.id == video_id
            )
        ).first()
        if not query:
            raise NotFound
        return query

    def get_all_photos(self):
        return self.get_all_items(LessonPhoto)