from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.users.models import User


class CourseCrud(BaseCrud):
    def create_new_course(self, course_data) -> None:
        news_item = Course(**course_data.dict())
        self.create_item(news_item)

    def get_all_items(self):
        return self.session.query(Course).all()

    def get_course_lessons(self, course_id):
        return self.session.query(Lesson).join(Course).filter(
            Lesson.course_id == course_id).all()

    def add_course_by_user(self, course_id: int, email: str):
        user = self.session.query(User).filter(
            User.email == email
        ).first()
        print(user)
        # course = self.session.query(Course).filter(
        #     Course.id == course_id
        # ).first()
        #
        # user.student.course.append(course)
        # self.session.add(user)
        # self.session.commit()
