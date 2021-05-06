from typing import List, Optional

from pydantic import BaseModel


class FilmBaseSchema(BaseModel):
    title: Optional[str] = None
    year: Optional[int] = None

    class Config:
        orm_mode = True


class FilmCreateSchema(FilmBaseSchema):
    title: str
    year: int


class FilmUpdateSchema(FilmBaseSchema):
    pass


class FilmSchema(FilmBaseSchema):
    title: str
    year: int
    id: int


class FilmListSchema(BaseModel):
    __root__: List[FilmSchema]


class FilmRatingSchema(BaseModel):
    rating: Optional[float] = None
    num_ratings: Optional[int] = None
    num_reviews: Optional[int] = None
