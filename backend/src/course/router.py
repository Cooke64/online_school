from fastapi import APIRouter, Path, Depends
from sqlalchemy.orm import Session

from src.auth.models import User
from src.course.crud import create_news_item
from src.course.models import Course
from src.course.shemas import CourseShow, CreateCourse
from src.database import get_db

router = APIRouter(tags=['Главная страничка курсов'])

dummy = [
    {'title': 'title', 'description': 'description', 'author': 3,
     'rating': 3,
     'lessons': [{
         'body': ' fake body'
     },
         {
             'body': ' fake body'
         },
         {
             'body': ' fake body'
         },
     ]
     },
    {'title': 'title', 'description': 'description', 'author': 3,
     'rating': 3,
     'lessons': [{
         'body': ' fake body'
     },
         {
             'body': ' fake body'
         },
         {
             'body': ' fake body'
         },
     ]
     },
    {'title': 'title', 'description': 'description', 'author': 3,
     'rating': 3,
     'lessons': [{
         'body': ' fake body'
     },
         {
             'body': ' fake body'
         },
         {
             'body': ' fake body'
         },
     ]
     }
]


@router.get('/{course_pk}', response_model=CourseShow)
def get_user_page(course_pk: int = Path(le=len(dummy))):
    if course_pk:
        return dummy[course_pk]
    return dummy


@router.post('/')
def get_user_page(course_data: CreateCourse,
                  db: Session = Depends(get_db)):
    # print(db.query(Course).first())
    create_news_item(db, course_data)
    return course_data
