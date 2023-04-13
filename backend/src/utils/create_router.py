from src.course.router import router as course_router
from src.lessons.router import router as lesson_router
from src.students.router import router as student_router
from src.users.router import router as user_router
from src.lesson_files.router import router as video_router
from src.main_page.router import router as main_router


def create_router(my_app):
    my_app.include_router(user_router)
    my_app.include_router(course_router)
    my_app.include_router(student_router)
    my_app.include_router(lesson_router)
    my_app.include_router(video_router)
    my_app.include_router(main_router)
