from sqlalchemy import desc, func

from src.course.models import Course, CourseRating
from src.database import BaseCrud
from src.students.models import StudentCourse


class MainCrud(BaseCrud):
    def get_three_popular(self):
        q = self.session.query(Course).join(StudentCourse)
        q = q.order_by(desc(StudentCourse.student_id)).limit(3).all()
        return q

    def get_three_withmax_raiting(self):
        q = self.session.query(Course).join(CourseRating)
        q = q.group_by(Course.id).order_by(desc(func.avg(CourseRating.rating))).limit(3).all()
        return q

    def top_free(self):
        q = self.session.query(Course).join(CourseRating)
        q = q.group_by(Course.id).order_by(desc(func.avg(CourseRating.rating))).filter(
            Course.is_free == True
        ).limit(3).all()
        return q
