from sqlalchemy.orm import Session

from src.course.models import Course, Lesson
from src.poll.models import Poll
from src.teachers.models import Teacher
from tests.utils.crud import (
    create_user,
    create_item,
    create_teacher,
    create_student)
from tests.utils.users import UserData

COURSE_DATA = {
    'title': 'title',
    'description': 'description',
    'is_free': True
}
LESSON_DATA = {
    "title": "string",
    "content": "string",
    'is_trial': True,
}

POLL_DATA = {
    "poll_description": "string"
}

USER_DATA = UserData('1@1.ru', '1', '1')
USER_DATA_INACTIVE = UserData('2@2.ru', '2', '2')


def create_free_courses(teacher, session: Session):
    for _ in range(2):
        new_item = Course(**COURSE_DATA)
        new_item.teachers.append(teacher)
        create_item(new_item, session)


def create_course_with_free_lessons(teacher: Teacher, session: Session):
    COURSE_DATA.update({'is_free': True})
    last_item = Course(**COURSE_DATA)
    last_item.teachers.append(teacher)
    last_course = create_item(last_item, session)
    for i in range(2):
        new_lesson = Lesson(
            course_id=last_course.id,
            **LESSON_DATA
        )
        create_item(new_lesson, session)


def create_not_free_course_with_not_free_lessons(
        teacher: Teacher, session: Session):
    COURSE_DATA.update({'is_free': True})
    course = Course(**COURSE_DATA)
    course.teachers.append(teacher)
    new_course = create_item(course, session)
    LESSON_DATA.update({'is_trial': False})
    new_lesson = Lesson(
        course_id=new_course.id,
        **LESSON_DATA
    )
    create_item(new_lesson, session)


def create_awards(sesssion: Session):
    return sesssion


def create_poll(session: Session):
    lessons_list: list[Lesson] = session.query(Lesson).all()
    for lesson in lessons_list:
        new_poll = Poll(lesson_id=lesson.id, **POLL_DATA)
        create_item(new_poll, session)


def create_fake_bd(session: Session):
    user = create_user(*USER_DATA, session=session)
    teacher = create_teacher(user.id, session)

    user_inactive = create_user(*USER_DATA_INACTIVE, session=session,
                                is_active=False, is_teacher=False)
    create_student(user_inactive.id, session)
    create_free_courses(teacher, session)
    create_course_with_free_lessons(teacher, session)
    create_not_free_course_with_not_free_lessons(teacher, session)
    create_poll(session)
