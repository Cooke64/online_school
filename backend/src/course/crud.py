from src.course.models import Course


def create_news_item(session, course_data) -> None:
    news_item = Course(**course_data.dict())
    session.add(news_item)
    session.commit()
