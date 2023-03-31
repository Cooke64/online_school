from sqlalchemy import and_
from sqlalchemy.orm import joinedload

from src.course.models import Course, Lesson
from src.database import BaseCrud
from src.exceptions import NotFound, PermissionDenied
from src.lessons.shemas import LessonBase
from src.students.models import StudentCourse
from src.users.models import User


class LessonCrud(BaseCrud):
    def get_all_course_lessons(self, course_id, user_email='2@2.com'):
        user = self.get_user_by_email(User, user_email)
        query: Course = self.session.query(Course).options(
            joinedload(Course.lessons)).where(
            Course.id == course_id).first()
        user_course: StudentCourse = self.session.query(StudentCourse).filter(
            and_(
                StudentCourse.course_id == course_id,
                StudentCourse.student_id == user.student.id
            )
        ).first()
        if all([user, query, user_course]):
            if user_course.has_paid or query.is_free:
                return query
            raise PermissionDenied
        raise NotFound

    def get_lesson_from_course(self, course_id, lessons_id):
        query = self.session.query(Lesson).join(Course).filter(and_(
            Course.id == course_id, Lesson.id == lessons_id
        )).first()
        if not query:
            raise NotFound
        return query

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
