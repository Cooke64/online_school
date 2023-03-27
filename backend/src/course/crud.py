from src.course.models import Course
from src.database import BaseCrud
from src.exceptions import NotFound
from src.students.models import Student
from src.users.models import User


class CourseCrud(BaseCrud):
    def create_new_course(self, course_data) -> None:
        news_item = Course(**course_data.dict())
        self.create_item(news_item)

    def get_all_items(self):
        query = self.session.query(Course).first()
        query.lessons
        return self.session.query(Course).all()

    def get_course_by_id(self, course_id):
        # Почему-то так выдается правильный ответ, где есть lessons в ответе
        query = self.session.query(Course).first()
        query.lessons
        query = self.session.query(Course).filter(
            Course.id == course_id
        ).first()
        if not query:
            raise NotFound
        return query

    def add_course_by_user(self, course_id: int, email: str):
        student = self.session.query(Student).join(User).filter(
            User.email == email
        ).first()
        course = self.get_course_by_id(course_id)
        student.courses.append(course)
        self.session.commit()

    def update_course(self, course_id, data_to_update):
        query = self.update_item(course_id, Course, data_to_update)
        if query:
            return query

    def delete_course(self, course_id):
        self.remove_item(course_id, Course)
        return {'deleted': 'Done'}
