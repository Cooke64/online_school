from fastapi import HTTPException, status

from src.course.models import Course
from src.database import BaseCrud
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
        return query

    def add_course_by_user(self, course_id: int, email: str):
        student = self.session.query(Student).join(User).filter(
            User.email == email
        ).first()
        course = self.get_course_by_id(course_id)
        student.courses.append(course)
        self.session.commit()
