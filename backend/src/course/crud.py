from sqlalchemy import func, exists, and_
from sqlalchemy.orm import joinedload

from src.auth.utils.auth_bearer import UserPermission
from src.course import exceptions as ex
from src.course.models import (
    Course,
    CourseRating,
    Lesson,
    CourseReview,
    CoursePreviewImage
)
from src.course.shemas import CreateCourse, ReviewBase
from src.course.utils import Rating
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

    def _get_course_rating(self, course_id: int) -> float | int:
        rating = self.session.query(func.avg(
            CourseRating.rating).label('average')).join(Course).filter(
            CourseRating.course_id == course_id).first()
        commas_after_ratig = 2
        if rating[0]:
            return round(rating[0], commas_after_ratig)
        return 0

    def add_rating_to_course(self, permission: UserPermission, course_id: int,
                             rating: Rating) -> None:
        """Добавление рейтинга курсу. Если уже рейтинг поставлен, то
        рейзит ошибку 400. В таком случае рейтинг можно удалить или обнавить.
        """
        student = self.get_student_by_email(permission.user_email).id
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

    def update_rating(self, permission: UserPermission, course_id: int,
                      new_rating: Rating) -> None:
        student = self.get_student_by_email(permission.user_email).id
        self.session.query(CourseRating).filter(and_(
            CourseRating.course_id == course_id,
            CourseRating.student_id == student)
        ).update({'rating': new_rating.value}, synchronize_session='fetch')
        self.session.commit()

    def create_new_course(
            self,
            course_data: CreateCourse,
            permission: UserPermission
    ) -> Course:
        """
        Создает новый курс.
            - Добавляет автора по его емейлу
            - Возвращает объект модели Course
        """
        print(course_data, 1)
        teacher = self.get_teacher_by_email(permission.user_email)
        new_item = Course(**course_data.dict())
        new_item.teachers.append(teacher)
        return self.create_item(new_item)

    def get_all_items(self) -> list[Course]:
        """Получить список всех курсов."""
        query: list[Course] = self.session.query(Course).options(
            joinedload(Course.course_preview)).options(
            joinedload(Course.reviews)).options(
            joinedload(Course.teachers).options(
                joinedload(Teacher.user))).all()
        return query

    def get_course_by_id(self, course_id: int) -> dict:
        """Получить CourseDetail по его id"""
        result = self.session.query(Course).options(
            joinedload(Course.course_preview)).options(
            joinedload(Course.lessons)).options(
            joinedload(Course.teachers).options(
                joinedload(Teacher.user))
        ).filter(Course.id == course_id).first()
        count_lessons = self.session.query(Lesson).filter(
            Lesson.course_id == course_id).count()
        if result:
            rating_to_show = self._get_course_rating(result.id)
            return {'course': result, 'rating': rating_to_show,
                    'count_lessons': count_lessons}
        raise ex.NotFoundCourse

    def _create_passed_lesson(self, student_id: int, lesson_id: int,
                              pass_=False):
        """Создает запись в бд, что студент прошел курс."""
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

    def add_course_by_user(self, course_id: int, permission: UserPermission):
        """
        Добавляет курс в список курсов студента.
        - передается емейл авторизованного пользователя, полученный по его токену.
        """
        student = self.get_student_by_email(permission.user_email)
        course = self.get_current_item(course_id, Course).first()
        if course in student.courses:
            raise ex.AddExisted
        student.courses.append(course)
        self.session.commit()
        if course.lessons:
            self._update_user_passed_lessons(student.id, course.lessons)

    def pay_for_course(self, course_id: int, permission: UserPermission):
        """Оплата курса пользователем. has_payd = True"""
        user = self.get_user_by_email(User, permission.user_email)
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

    def update_course(self,
                      course_id: int,
                      data_to_update,
                      permission: UserPermission):
        course = self.get_current_item(course_id, Course).first()
        teacher = self.get_teacher_by_email(permission.user_email)
        if teacher not in course.teachers:
            raise ex.HasNotPermission
        query = self.update_item(course_id, Course, data_to_update)
        if query:
            return query

    def delete_course(self, course_id: int, permission: UserPermission):
        course = self.get_current_item(course_id, Course).first()
        teacher = self.get_teacher_by_email(permission.user_email)
        if teacher not in course.teachers:
            raise ex.HasNotPermission
        self.remove_item(course_id, Course)

    def remove_course_from_list(self, course_id: int,
                                permission: UserPermission):
        """Удаление пользователем курса из добавленных в список для прохождения."""
        course = self.get_current_item(course_id, Course).first()
        student = self.get_student_by_email(permission.user_email)
        if course not in student.courses:
            raise ex.NotFoundCourse
        student.courses.remove(course)
        self.create_item(student)

    def add_review_to_course(
            self,
            course_id: int,
            permission: UserPermission,
            text: ReviewBase
    ):
        """Добавить отзыв на курс."""
        course = self.get_current_item(course_id, Course).first()
        student = self.get_student_by_email(permission.user_email)
        new_review = CourseReview(
            student_id=student.id, course_id=course.id, text=text.text)
        self.create_item(new_review)

    def delete_review(
            self,
            permission: UserPermission,
            review_id: int,
            course_id: int
    ):
        review: CourseReview = self.get_current_item(review_id,
                                                     CourseReview).first()
        student = self.get_student_by_email(permission.user_email)
        if not (
                review.student_id == student.id and review.course_id == course_id):
            raise ex.HasNotPermission
        self.remove_item(review.id, CourseReview)

    def add_preview(
            self,
            course_id: int,
            file_obj: bytes,
            file_type: str,
            teacher_emal: str = '1@1.com'):
        """Добавить фото превью к уроку."""
        course: Course = self.get_current_item(course_id, Course).first()
        teacher = self.get_teacher_by_email(teacher_emal)
        if teacher not in course.teachers:
            raise ex.HasNotPermission
        if course.course_preview:
            course_prev: CoursePreviewImage = self.get_current_item(
                course.course_preview.id, CoursePreviewImage).first()
            course_prev.photo_blob = file_obj
            course_prev.photo_typee = file_type
            self.session.commit()
            return
        item = CoursePreviewImage(
            photo_blob=file_obj,
            photo_type=file_type,
            course_id=course_id
        )
        self.create_item(item)
