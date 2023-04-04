from src.database import BaseCrud
from src.lesson_files.models import LessonContent, LessonPhoto, LessonVideo


class MediaCrud(BaseCrud):

    def upload_content(
            self,
            blob: bytes,
            file_type: str,
            course_id: int = 1,
            photo_content: bool = True
    ):
        new_lesson_content = LessonContent(course_id=course_id)
        lesson_content_id = self.create_item(new_lesson_content)
        if photo_content:
            lesson_photo = LessonPhoto(
                photo_blob=blob,
                photo_type=file_type,
                lesson_content_id=lesson_content_id.id
            )
            self.create_item(lesson_photo)
        else:
            lesson_photo = LessonVideo(
                video_blob=blob,
                lesson_content_id=lesson_content_id.id,
                video_type=file_type,
            )
            self.create_item(lesson_photo)

    def get_contnent(self, content_id, photo: bool = True) -> LessonPhoto | LessonVideo:
        model = LessonPhoto if photo else LessonVideo
        return self.get_current_item(content_id, model).first()

    def get_all_photos(self):
        return self.get_all_items(LessonPhoto)