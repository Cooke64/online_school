from sqlalchemy import and_

from src.course.models import Lesson, Course
from src.main_crud import BaseCrud
from src.exceptions import NotFound, PermissionDenied, NotAuthenticated
from src.lesson_files.models import LessonPhoto, LessonVideo
from src.lesson_files.constants import ErrorCode as ex


class MediaCrud(BaseCrud):
    def check_lesson_teacher(self, lesson_id: int):
        """Проверка, что действительно есть такой курс с таким lesson_id
         пользователь имеет статус преподавателя и входит в число
         преподавателй-создателей курса"""
        course = self.session.query(Course).join(Lesson).filter(
            Lesson.id == lesson_id
        ).first()
        if not course:
            return self.get_json_reposnse(*ex.NOT_FOUND_COURSE)
        if not self.user:
            raise NotAuthenticated
        if self.user.teacher not in course.teachers:
            return self.get_json_reposnse(*ex.HAS_NOT_RIGHT)

    def upload_content(
            self,
            blob: bytes,
            file_type: str,
            lesson_id: int,
            photo_content: bool = True
    ):
        if photo_content:
            lesson_photo = LessonPhoto(
                photo_blob=blob,
                photo_type=file_type,
                lesson_content_id=lesson_id
            )
            self.create_item(lesson_photo)
        else:
            lesson_photo = LessonVideo(
                video_blob=blob,
                lesson_content_id=lesson_id,
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

    def remove_photo(
            self, photo_id: int, lesson_id: int,
    ):
        self.check_lesson_teacher(lesson_id)
        photo = self.get_photo_item(photo_id, lesson_id)
        if not self.is_teacher or not self.is_staff:
            raise PermissionDenied
        self.remove_item(photo.id, LessonPhoto)
