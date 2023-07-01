from sqlalchemy import func, and_
from sqlalchemy.orm import joinedload

from src.course.models import Course, CourseRating, CourseReview, Lesson
from src.database import BaseCrud
from src.lessons.models import LessonComment
from src.students.models import StudentCourse
from src.teachers.models import Teacher, TeacherCourse
from src.users.models import User


class TeachersCrud(BaseCrud):
    def _count_courses(self, teacher_id: int) -> int:
        """Возвращает количество курсов преподавателя."""
        return self.session.query(TeacherCourse).filter(
            TeacherCourse.user_id == teacher_id).count()

    def _get_total_rating(self, teacher_id: int,
                          courses: list[Course]) -> float | int:
        teacher_courses = self._count_courses(teacher_id)
        all_courses_rating = 0
        commas_after_ratig = 2
        for course in courses:
            rating = self.session.query(func.avg(
                CourseRating.rating).label('average')).join(Course).filter(
                CourseRating.course_id == course.id).first()
            if rating[0]:
                all_courses_rating += round(rating[0], commas_after_ratig)
        return round(all_courses_rating / teacher_courses,
                     commas_after_ratig) if teacher_courses else 0

    def _get_total_reviews(self, courses: list[Course]) -> int:
        res = 0
        for course in courses:
            res += self.session.query(CourseReview).filter(
                CourseReview.course_id == course.id).count()
        return res

    def _create_teacher_stats(self, teacher: Teacher) -> dict:
        teacher_dict = {'teacher_info': teacher}
        teacher_dict.update(
            {'count_courses': self._count_courses(teacher.id)})
        teacher_dict.update(
            {'total_reviews': self._get_total_reviews(teacher.courses)})
        teacher_dict.update(
            {'total_rating': self._get_total_rating(
                teacher.id, teacher.courses)})
        return teacher_dict

    def get_teachers_data(self) -> list[dict]:
        teachers_list = []
        teachers: list[Teacher] = self.session.query(Teacher).options(
            joinedload(Teacher.user)).options(
            joinedload(Teacher.courses)).all()
        for teacher in teachers:
            teacher_dict = self._create_teacher_stats(teacher)
            teachers_list.append(teacher_dict)
        return teachers_list

    def get_teacher_detail(self, teacher_id):
        teacher: Teacher = self.session.query(Teacher).options(
            joinedload(Teacher.user)).options(
            joinedload(Teacher.courses)).filter(
            Teacher.id == teacher_id).first()

        teacher_statics = self._create_teacher_stats(teacher)
        return teacher_statics


class TeacherProfileCrud(TeachersCrud):
    def _get_teacher_courses(self, user: User) -> list[Course]:
        return self.session.query(Teacher).options(
            joinedload(Teacher.courses)).filter(
            Teacher.user == user).all()

    def _count_comments(self, courses: list[Course]) -> int:
        res = 0
        for course in courses:
            res += self.session.query(LessonComment).join(Lesson).filter(
                Lesson.course_id == course.id).count()
        return res

    def _count_pucrchased_courses(self, teacher: Teacher) -> int:
        return self.session.query(StudentCourse).join(Course).filter(and_(
            StudentCourse.has_paid == True,
            Course.teachers.contains(teacher)
        )).count()

    def get_teacher_profile(self):
        teacher = self.teacher
        courses = self._get_teacher_courses(teacher)
        result = {
            'courses': courses,
            'count_comments': self._count_comments(courses),
            'avg_rating': self._get_total_rating(teacher.id, courses),
            'purchased_courses': self._count_pucrchased_courses(teacher)
        }
        return result
