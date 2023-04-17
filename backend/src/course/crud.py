from sqlalchemy import func, exists, and_
from sqlalchemy.orm import joinedload

from src.auth.utils.auth_bearer import UserPermission
from src.course import exceptions as ex
from src.course.models import Course, CourseRating, Lesson, CourseReview
from src.course.shemas import CreateCourse, ReviewBase
from src.database import BaseCrud
from src.students.models import Student, StudentCourse, StudentPassedLesson
from src.teachers.models import Teacher
from src.users.models import User


class CourseCrud(BaseCrud):
    def get_teacher_by_email(self, email: str) -> Teacher:
        teacher = self.session.query(
            Teacher).join(User).filter(
            User.email == email).first()
        if not teacher:
            raise ex.NotFoundTeacher
        return teacher

    def get_student_by_email(self, email: str) -> Student:
        student = self.session.query(
            Student).join(User).filter(
            User.email == email
        ).first()
        if not student:
            raise ex.NotFoundStudent
        return student

    def _get_course_rating(self, course_id) -> float | int:
        rating = self.session.query(func.avg(
            CourseRating.rating).label('average')).join(Course).filter(
            CourseRating.course_id == course_id).first()
        commas_after_ratig = 2
        if rating[0]:
            return round(rating[0], commas_after_ratig)
        return 0

    def add_rating_to_course(self, user_email, course_id, rating):
        """Добавление рейтинга курсу. Если уже рейтинг поставлен, то
        рейзит ошибку 400. В таком случае рейтинг можно удалить или обнавить.
        """
        student = self.get_student_by_email(user_email).id
        course = self.get_current_item(course_id, Course).first()
        if self.session.query(exists().where(and_(
                CourseRating.course_id == course_id,
                CourseRating.student_id == student)
        )).scalar():
            raise ex.AddExisted
        if not course:
            raise ex.NotFoundCourse
        course_rating = CourseRating(
            student_id=student, course_id=course.id, rating=rating.value)
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
            user_email: str
    ) -> Course:
        """
        Создает новый курс.
            - Добавляет автора по его емейлу
            - Возвращает объект модели Course
        """
        teacher = self.get_teacher_by_email(user_email)
        if not teacher:
            raise ex.NotFoundTeacher
        new_item = Course(**course_data.dict())
        new_item.teachers.append(teacher)
        return self.create_item(new_item)

    def get_all_items(self) -> list[Course]:
        query = self.session.query(Course).options(
            joinedload(Course.reviews)).options(
            joinedload(Course.teachers).options(
                joinedload(Teacher.user))).all()
        return query

    def get_course_by_id(self, course_id: int) -> dict:
        result = self.session.query(Course).options(
            joinedload(Course.lessons)).options(
            joinedload(Course.teachers).options(
                joinedload(Teacher.user))
        ).filter(Course.id == course_id).first()
        if result:
            rating_to_show = self._get_course_rating(result.id)
            return {'course': result, 'rating': rating_to_show}
        raise ex.NotFoundCourse

    def _create_passed_lesson(self, student_id, lesson_id, pass_=False):
        open_lesson = StudentPassedLesson(
            student_id=student_id,
            lesson_id=lesson_id,
            has_pass=pass_,
            when_pass=func.current_date()
        )
        self.create_item(open_lesson)

    def _update_user_passed_lessons(
            self, student_id: int, lessons_list: list[Lesson]
    ) -> None:
        if lessons_list:
            first_lesson = lessons_list[0]
            self._create_passed_lesson(student_id, first_lesson.id, True)
            for num in range(1, len(lessons_list)):
                lesson_item = lessons_list[num]
                self._create_passed_lesson(student_id, lesson_item.id)

    def add_course_by_user(self, course_id: int, email: str):
        """
        Добавляет курс в список курсов студента.
        :param course_id: первичный ключ выбранного курса.
        :param email: email пользователя.
            - передается емейл авторизованного пользователя, полученный по его токену.
        """
        student = self.get_student_by_email(email)
        course = self.get_current_item(course_id, Course).first()
        if not course:
            raise ex.NotFoundCourse
        if course in student.courses:
            raise ex.AddExisted
        student.courses.append(course)
        self.session.commit()
        if course.lessons:
            self._update_user_passed_lessons(student.id, course.lessons)

    def pay_for_course(self, course_id, user_email):
        """Оплата курса пользователем. has_payd = True"""
        user = self.get_user_by_email(User, user_email)
        if user:
            user_course = self.session.query(
                StudentCourse).filter(
                and_(
                    StudentCourse.course_id == course_id,
                    StudentCourse.student_id == user.student.id
                )
            )
            if user_course.first().has_paid:
                return {'result': 'Уже оплачено'}
            user_course.update({'has_paid': True}, synchronize_session='fetch')
            self.session.commit()
            return {'result': 'Оплачено'}
        raise ex.NotFoundStudent

    def update_course(self,
                      course_id: int,
                      data_to_update,
                      permission: UserPermission):
        course = self.get_current_item(course_id, Course).first()
        teacher = self.get_teacher_by_email(permission.user_email)
        if not course:
            raise ex.NotFoundCourse
        if teacher not in course.teachers:
            raise ex.HasNotPermission
        query = self.update_item(course_id, Course, data_to_update)
        if query:
            return query

    def delete_course(self, course_id: int, permission: UserPermission):
        course = self.get_current_item(course_id, Course).first()
        teacher = self.get_teacher_by_email(permission.user_email)
        if not course:
            raise ex.NotFoundCourse
        if teacher not in course.teachers:
            raise ex.HasNotPermission
        self.remove_item(course_id, Course)

    def remove_course_from_list(self, course_id: int, user_email: str):
        """Удаление пользователем курса из добавленных в список для прохождения."""
        course = self.get_current_item(course_id, Course).first()
        student = self.get_student_by_email(user_email)
        if course not in student.courses:
            raise ex.NotFoundCourse
        student.courses.remove(course)
        self.create_item(student)

    def add_review_to_course(
            self,
            course_id: int,
            user_email: str,
            text: ReviewBase
    ):
        """Добавить отзыв на курс."""
        course = self.get_current_item(course_id, Course).first()
        student = self.get_student_by_email(user_email)
        new_review = CourseReview(student_id=student.id, course_id=course.id,
                                  text=text.text)
        self.create_item(new_review)

    def delete_review(
            self,
            user_email: str,
            review_id: int,
            course_id: int
    ):
        review: CourseReview = self.get_current_item(review_id, CourseReview).first()
        student = self.get_student_by_email(user_email)
        if not (review.student_id == student.id and review.course_id == course_id):
            raise ex.HasNotPermission
        self.remove_item(review.id, CourseReview)
