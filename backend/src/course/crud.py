from src.course.models import Course, Lesson
from src.database import BaseCrud


class CourseCrud(BaseCrud):
    def create_news_item(self, course_data) -> None:
        news_item = Course(**course_data.dict())
        self.create_item(news_item)

    def get_all_items(self):
        return self.session.query(Course).all()

    def get_course_lessons(self, course_id):
        return self.session.query(Lesson).join(Course).filter(
            Lesson.course_id == course_id).all()
