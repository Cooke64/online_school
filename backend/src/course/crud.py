from sqlalchemy import func, exists, and_
from sqlalchemy.orm import joinedload

from src.course import exceptions as ex
from src.course.models import (
    Course,
    CourseRating,
    Lesson,
    CourseReview,
    CoursePreviewImage
)
from src.course.shemas import CreateCourse, ReviewBase, UpdateCourse
from src.course.utils import Rating
from src.database import BaseCrud
from src.exceptions import PermissionDenied
from src.students.models import StudentCourse, StudentPassedLesson
from src.teachers.models import Teacher


class CourseCrud(BaseCrud):
    def __get_course_rating(self, course_id: int) -> float | int:
        rating = self.session.query(func.avg(
            CourseRating.rating)).filter(
            CourseRating.course_id == course_id).first()
        # количество запятых для округления значения рейтинга
        commas_after_ratig = 2
        if rating[0]:
            return round(rating[0], commas_after_ratig)
        return 0

    def __update_rating(self, course_id: int,
                        new_rating: Rating) -> None:
        student = self.student
        self.session.query(CourseRating).filter(and_(
            CourseRating.course_id == course_id,
            CourseRating.student_id == student.id)
        ).update({'rating': new_rating.value}, synchronize_session='fetch')
        self.session.commit()

    def add_rating_to_course(self, course_id: int,
                             rating: Rating) -> None:
        """Добавление рейтинга курсу. Если уже рейтинг поставлен, то
        рейзит ошибку 400. В таком случае рейтинг можно удалить или обнавить.
        """
        student = self.student
        course = self.get_current_item(course_id, Course).first()
        if self.session.query(exists().where(and_(
                CourseRating.course_id == course_id,
                CourseRating.student_id == student.id)
        )).scalar():
            self.__update_rating(course_id, rating)
            return
        if not course:
            raise ex.NotFoundCourse
        course_rating = CourseRating(
            student_id=student.id, course_id=course.id, rating=rating.value)
        self.create_item(course_rating)

    def create_new_course(
            self,
            course_data: CreateCourse,
    ) -> Course:
        """
        Создает новый курс.
            - Добавляет автора по его емейлу
            - Возвращает объект модели Course
        """
        if not self.is_teacher:
            raise PermissionDenied
        teacher = self.teacher
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

    def get_course_by_id(self, course_id: int):
        """Получить CourseDetail по его id"""
        result: Course = self.session.query(Course).options(
            joinedload(Course.lessons)).options(
            joinedload(Course.teachers).options(
                joinedload(Teacher.user))
        ).filter(Course.id == course_id).first()
        count_lessons: int = self.session.query(Lesson).filter(
            Lesson.course_id == course_id).count()
        if result:
            rating_to_show = self.__get_course_rating(result.id)
            return {
                'course': result,
                'rating': rating_to_show,
                'count_lessons': count_lessons
            }
        raise ex.NotFoundCourse

    def __create_passed_lesson(self, student_id: int, lesson_id: int,
                               pass_=False):
        """Создает запись в бд, что студент прошел урок."""
        passed_lesson = self.session.query(StudentPassedLesson).filter(
            StudentPassedLesson.student_id == student_id,
            StudentPassedLesson.lesson_id == lesson_id
        ).first()
        if not passed_lesson:
            open_lesson = StudentPassedLesson(
                student_id=student_id,
                lesson_id=lesson_id,
                has_pass=pass_,
                when_pass=func.current_date()
            )
            self.create_item(open_lesson)

    def __update_user_passed_lessons(
            self, student_id: int, lessons_list: list[Lesson] | None
    ) -> None:
        """При добавлении курса пользователем добавляет запись в БД, что
            пользователь прошел первый урок, который становится доступный
            ему для открытия и просмотра. Остальные уроки курса добавляются
            с пометкой has_pass=False
        """
        if lessons_list:
            first_lesson = lessons_list[0]
            self.__create_passed_lesson(student_id, first_lesson.id, True)
            for num in range(1, len(lessons_list)):
                lesson_item = lessons_list[num]
                self.__create_passed_lesson(student_id, lesson_item.id)

    def add_course_by_user(self, course_id: int):
        """
        Добавляет курс в список курсов студента.
        """
        student = self.student
        course = self.get_current_item(course_id, Course).first()
        if course in student.courses:
            raise ex.AddExisted
        student.courses.append(course)
        self.session.commit()
        if course.lessons:
            self.__update_user_passed_lessons(student.id, course.lessons)

    def pay_for_course(self, course_id: int):
        """Оплата курса пользователем. has_payd = True"""
        user = self.user
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
        raise ex.PermissionDenied

    def update_course(self,
                      course_id: int,
                      data_to_update: UpdateCourse,
                      ) -> Course:
        course = self.get_current_item(course_id, Course).first()
        teacher = self.teacher
        if teacher not in course.teachers:
            raise ex.HasNotPermission
        return self.update_item(course_id, Course, data_to_update)

    def delete_course(self, course_id: int):
        course = self.get_current_item(course_id, Course).first()
        teacher = self.teacher
        if teacher in course.teachers or self.is_staff:
            self.remove_item(course_id, Course)
            return self.get_json_reposnse('Курс удален', 204)
        raise ex.HasNotPermission

    def remove_course_from_list(self, course_id: int):
        """Удаление пользователем курса из добавленных в список для прохождения."""
        course = self.get_current_item(course_id, Course).first()
        student = self.student
        if course not in student.courses:
            raise ex.NotFoundCourse
        student.courses.remove(course)
        self.create_item(student)

    def add_review_to_course(
            self,
            course_id: int,
            text: ReviewBase
    ):
        """Добавить отзыв на курс."""
        if not self.is_student:
            raise PermissionDenied
        course = self.get_current_item(course_id, Course).first()
        student = self.student
        new_review = CourseReview(
            student_id=student.id, course_id=course.id, text=text.text)
        self.create_item(new_review)

    def delete_review(
            self,
            course_id: int
    ):
        student = self.student
        if not self.is_student or not self.is_staff:
            raise ex.HasNotPermission
        review = self.session.query(CourseReview).filter(
            CourseReview.course_id == course_id,
            CourseReview.student_id == student.id
        ).first()
        if not review:
            raise ex.NotFoundObject
        self.remove_item(review.id, CourseReview)

    def add_preview(
            self,
            course_id: int,
            file_obj: bytes,
            file_type: str, ):
        """Добавить фото превью к уроку."""
        course: Course = self.get_current_item(course_id, Course).first()
        if course.course_preview:
            course_prev = self.get_current_item(
                course.course_preview.id, CoursePreviewImage
            ).first()
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

    def add_course_in_favorite(self, course_id: int):
        """Добавить курс в избранные для пользователя.
            - Если курс находится в избранных, то райзится ошибка
            - Может быть доступно для пользователя со статусом Student
        """

        student = self.student
        course = self.get_current_item(course_id, Course).first()
        if course in student.favorite_courses:
            raise ex.AddExisted
        student.favorite_courses.append(course)
        self.session.commit()
        return self.get_json_reposnse('Курс добавлен в избранное', 201)

    def remove_course_from_favorite(self, course_id: int):
        """Удалить курс из избранных для пользователя.
            - Если курса нет в избранных, то райзится ошибка
            - Может быть доступно для пользователя со статусом Student
        """
        student = self.student
        course = self.get_current_item(course_id, Course).first()
        if course not in student.favorite_courses:
            raise ex.NotFoundCourse
        student.favorite_courses.remove(course)
        self.create_item(student)
        return self.get_json_reposnse('Курс удален из избранных', 204)
