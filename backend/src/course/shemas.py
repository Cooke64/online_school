from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    title: str
    description: str
    author_id: int

    class Config:
        orm_mode = True


class LessonBase(BaseModel):
    body: str


class CourseShow(CourseBase):
    lessons: list[LessonBase] | None = []
    rating: int


class CreateCourse(CourseBase):
    rating: int = Field(
        gt=0, le=5,
        title="The rating of the current curse",
        description="The rating must be greater than zero and equal or less than five"
    )

    class Config:
        schema_extra = {
            "example": {
                "author_id": 1, 'title': 'title',
                "description": 'description',
                'rating': 4
            }
        }
