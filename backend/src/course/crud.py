from src.course.models import Course
from src.course.shemas import CreateCourse
from src.database import BaseCrud
from src.exceptions import NotFound
from src.students.models import Student
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
        course = self.session.query(Course).first()
        if course:
            course.lessons
            [t.user.username for t in course.teachers]
            return self.session.query(Course).all()
        return None

    def get_course_by_id(self, course_id: int) -> Course:
        # Почему-то так выдается правильный ответ, где есть lessons в ответе
        query = self.session.query(Course).first()
        query.lessons
        query = self.session.query(Course).filter(
            Course.id == course_id
        ).first()
        if not query:
            raise NotFound
        return query

    def add_course_by_user(self, course_id: int, email: str):
        """
        Добавляет курс в список курсов студента.
        :param course_id: первичный ключ выбранного курса.
        :param email: email пользователя.
            - передается емейл авторизованного пользователя, полученный по его токену.
        """
        student = self.get_student_by_email(email)
        course = self.get_course_by_id(course_id)
        student.courses.append(course)
        self.session.commit()

    def update_course(self, course_id, data_to_update):
        query = self.update_item(course_id, Course, data_to_update)
        if query:
            return query

    def delete_course(self, course_id: int):
        self.remove_item(course_id, Course)

    def remove_course_from_list(self, course_id: int, user_email: str):
        course = self.get_course_by_id(course_id)
        student = self.get_student_by_email(user_email)
        if course not in student.courses:
            raise NotFound
        student.courses.remove(course)
        self.create_item(student)



