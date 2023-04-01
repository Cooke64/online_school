# from sqlalchemy.orm import relationship
#
# from src.database import BaseModel
# import sqlalchemy as sa
#
#
# class LessonContent(BaseModel):
#     __tablename__ = 'lessons_contents'
#     description = sa.Column(sa.Text, nullable=False)
#     pictures = relationship('LessonPhotos', back_populates='lesson_content')
#
#
# class LessonPhotos(BaseModel):
#     __tablename__ = 'lessons_photos'
#     photo_id = sa.Column(sa.String(199), nullable=False)
#