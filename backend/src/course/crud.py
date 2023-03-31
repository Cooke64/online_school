from sqlalchemy import func, exists, and_
from sqlalchemy.orm import joinedload

from src.course.models import Course, CourseRating
from src.course.shemas import CreateCourse
from src.database import BaseCrud
from src.exceptions import NotFound, BadRequest
from src.students.models import Student, StudentCourse
from src.teachers.models import Teacher
from src.users.models import User


class CourseCrud(BaseCrud):
    def get_teacher_by_email(self, email: str) -> Teacher:
        teacher = self.session.query(
            Teacher).join(User).filter(
            User.email == email).first()
        if not teacher:
            raise NotFound
        return teacher

    def get_student_by_email(self, email: str) -> Student:
        student = self.session.query(
            Student).join(User).filter(
            User.email == email
        ).first()
        if not student:
            raise NotFound
        return student

    def _get_course_rating(self, course_id):
        rating = self.session.query(func.avg(
            CourseRating.rating).label('average')).join(Course).filter(
            CourseRating.course_id == course_id).first()
        if rating[0]:
            return round(rating[0], 2)
        return 0

    def add_rating_to_course(self, user_email, course_id, rating):
        student = self.get_student_by_email(user_email).id
        course = self.get_current_item(course_id, Course).first()
        if self.session.query(exists().where(and_(
                CourseRating.course_id == course_id,
                CourseRating.student_id == student)
        )).scalar():
            raise BadRequest()
        if not course:
            raise NotFound
        course_rating = CourseRating(
            student_id=student,
            course_id=course.id,
            rating=rating.value)
        self.create_item(course_rating)

    def update_rating(self, user_email, course_id, new_rating):
        student = self.get_student_by_email(user_email).id
        self.session.query(CourseRating).filter(and_(
            CourseRating.course_id == course_id,
            CourseRating.student_id == student)
        ).update({'rating': new_rating.value}, synchronize_session='fetch')
        self.session.commit()

    def create_new_course(
            self,
            course_data: CreateCourse,
            teacher: Teacher) -> Course:
        """
        Создает новый курс.
            - Добавляет автора по его емейлу
            - Возвращает объект модели Course
        """
        new_item = Course(**course_data.dict())
        new_item.teachers.append(teacher)
        return self.create_item(new_item)

    def get_all_items(self) -> list[Course] | None:
        return self.session.query(Course).options(joinedload(Course.students)).all()

    def get_course_by_id(self, course_id: int):
        query = self.session.query(Course).options(joinedload(Course.teachers).options(joinedload(Teacher.user))).where(Course.id == course_id).first()

        query.lessons
        rating_to_show = self._get_course_rating(query.id)
        return {'course': query, 'rating': rating_to_show}

    def add_course_by_user(self, course_id: int, email: str):
        """
        Добавляет курс в список курсов студента.
        :param course_id: первичный ключ выбранного курса.
        :param email: email пользователя.
            - передается емейл авторизованного пользователя, полученный по его токену.
        """
        student = self.get_student_by_email(email)
        course = self.get_current_item(course_id, Course).first()
        student.courses.append(course)
        self.session.commit()

    def pay_for_course(self, course_id, user_email):
        user = self.get_user_by_email(User, user_email)
        course = self.get_current_item(course_id, Course)
        if user and course:
            self.session.query(StudentCourse).filter(and_(
                StudentCourse.course_id == course.id,
                StudentCourse.student_id == user.student.id)
            ).update({'has_paid': True}, synchronize_session='fetch')
            return
        raise NotFound

    def update_course(self, course_id, data_to_update):
        query = self.update_item(course_id, Course, data_to_update)
        if query:
            return query

    def delete_course(self, course_id: int):
        self.remove_item(course_id, Course)

    def remove_course_from_list(self, course_id: int, user_email: str):
        course = self.get_current_item(course_id, Course).first()
        student = self.get_student_by_email(user_email)
        if course not in student.courses:
            raise NotFound
        student.courses.remove(course)
        self.create_item(student)
