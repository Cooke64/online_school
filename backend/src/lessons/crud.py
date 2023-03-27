from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.lessons.shemas import LessonBase


class LessonCrud(BaseCrud):
    def get_all_lessons(self):
        return self.get_all_items(Lesson)

    def create_lesson_instanse(self, course_id, lesson: LessonBase):
        new_lesson = Lesson(
            course_id=course_id,
            **lesson.dict()
        )
        result = self.create_item(new_lesson)
        return result

    def add_lesson_to_course(
            self, course_id: int,
            lesson_data: LessonBase = None
    ) -> None:
        if self.check_item_exists(course_id, Course):
            query = self.get_current_item(course_id, Course).first()
            lesson = self.create_lesson_instanse(query.id, lesson_data)
            return lesson
