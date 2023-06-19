"""
Здесь находятся endpoints для отображения и работы с опросами после прохождения урок.
Так же здесь находятся endpoints для работы с вопросами к опросу.
"""
from fastapi import APIRouter, Depends

from src.poll.crud import PollCrud
from src.poll.schemas import (
    PollBase,
    QuestionBase,
    AddAnswers,
    ShowLessonPoll,
    AddPoll
)

router = APIRouter(prefix='/poll', tags=['Опрос'])


@router.get('/')
def get_main(poll_crud: PollCrud = Depends()):
    return poll_crud.get_all_polls()


@router.post('/create_poll/{course_id}/{lesson_id}',
             summary='Создать новый опрос к уроку', )
def create_poll(
        course_id: int,
        lesson_id: int,
        poll_data: PollBase,
        poll_crud: PollCrud = Depends()):
    return poll_crud.add_poll_to_lesson(course_id, lesson_id, poll_data)


@router.delete('/remove_poll/{course_id}/{lesson_id}',
               summary='Удалить опрос', )
def remove_poll(
        lesson_id: int,
        poll_crud: PollCrud = Depends()):
    return poll_crud.remove_poll(lesson_id)


@router.post('/add_question/{poll_id}',
             summary='Добавить вопрос к опросу')
def add_question_to_poll(
        poll_id: int,
        question: QuestionBase,
        poll_crud: PollCrud = Depends()):
    return poll_crud.add_question(poll_id, question)


@router.post('/add_answers/{poll_id}/{question_id}',
             summary='Добавить ответы к вопросу в опросе')
def add_question_to_poll(
        poll_id: int,
        question_id: int,
        answers_list: AddAnswers,
        poll_crud: PollCrud = Depends()):
    """Позволяет добавить неограниченный список ответов к вопросу
    Ответ содержит в себе тело ответа и булевую переменную, обозначающую истинность овтета.
    """
    return poll_crud.add_answers_list(poll_id, question_id, answers_list)


@router.get('/lesson_poll/{lesson_id}',
            summary='Получить опрос к уроку курса',
            response_model=ShowLessonPoll)
def get_poll_from_lessons(
        lesson_id: int,
        poll_crud: PollCrud = Depends()):
    return poll_crud.get_lesson_poll(lesson_id)


@router.post('/add_poll/{course_id}/{lesson_id}',
             summary='Создать новый опрос c вопросами и ответами', )
def add_poll(
        course_id: int,
        lesson_id: int,
        poll_data: AddPoll,
        poll_crud: PollCrud = Depends()):
    return poll_crud.add_new_poll(course_id, lesson_id, poll_data)
