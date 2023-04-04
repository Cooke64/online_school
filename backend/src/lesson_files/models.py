from sqlalchemy.orm import relationship

from src.database import BaseModel
import sqlalchemy as sa


class LessonContent(BaseModel):
    __tablename__ = 'lessons_contents'
    course_id = sa.Column(sa.Integer, nullable=False)
    videos = relationship('LessonVideo', back_populates='lesson_content')
    photos = relationship('LessonPhoto', back_populates='lesson_content')


class LessonVideo(BaseModel):
    __tablename__ = 'lessons_videos'
    video_blob = sa.Column(sa.LargeBinary, nullable=False)
    video_type = sa.Column(sa.String, nullable=True)
    lesson_content_id = sa.Column(
        sa.Integer, sa.ForeignKey('lessons_contents.id')
    )
    lesson_content = relationship('LessonContent', back_populates='videos')


class LessonPhoto(BaseModel):
    __tablename__ = 'lessons_photos'
    photo_blob = sa.Column(sa.LargeBinary, nullable=False)
    photo_type = sa.Column(sa.String, nullable=True)
    lesson_content_id = sa.Column(
        sa.Integer, sa.ForeignKey('lessons_contents.id'))
    lesson_content = relationship('LessonContent', back_populates='photos')
