from sqlalchemy.orm import relationship


import sqlalchemy as sa

from src.BaseModel import BaseModel


class LessonVideo(BaseModel):
    __tablename__ = 'lessons_videos'
    video_blob = sa.Column(sa.LargeBinary, nullable=False)
    video_type = sa.Column(sa.String, nullable=True)
    lesson_content_id = sa.Column(
        sa.Integer, sa.ForeignKey('lessons.id')
    )
    lesson_content = relationship('Lesson', back_populates='videos')


class LessonPhoto(BaseModel):
    __tablename__ = 'lessons_photos'
    photo_blob = sa.Column(sa.LargeBinary, nullable=False)
    photo_type = sa.Column(sa.String, nullable=True)
    lesson_content_id = sa.Column(
        sa.Integer, sa.ForeignKey('lessons.id'))
    lesson_content = relationship('Lesson', back_populates='photos')
