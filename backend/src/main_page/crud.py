from sqlalchemy import desc, func
from sqlalchemy.orm import joinedload

from src.course.models import Course, CourseRating
from src.main_crud import BaseCrud
from src.lessons.models import LessonComment
from src.students.models import StudentCourse, Student


class MainCrud(BaseCrud):
    def get_three_popular(self):
        q = self.session.query(Course).join(StudentCourse)
        q = q.order_by(desc(StudentCourse.student_id)).limit(3).all()
        return q

    def get_three_withmax_raiting(self):
        q = self.session.query(Course).join(CourseRating)
        q = q.group_by(Course.id).order_by(
            desc(func.avg(CourseRating.rating))).limit(3).all()
        return q

    def top_free(self):
        q = self.session.query(Course).join(CourseRating)
        q = q.group_by(Course.id).order_by(
            desc(func.avg(CourseRating.rating))).filter(
            Course.is_free == True
        ).limit(3).all()
        return q

    def top_commentators(self):
        q = self.session.query(LessonComment).options(
            joinedload(LessonComment.student).options(
                joinedload(Student.user))
        )
        return q.all()

    def get_main_page_repsonse(self):
        response = {
            'popular': self.get_three_popular(),
            'rating': self.get_three_withmax_raiting(),
            'top_free': self.top_free(),
            'top_comentators': self.top_commentators()
        }
        return response
