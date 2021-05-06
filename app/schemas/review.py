from typing import List, Optional

from pydantic import BaseModel, Field


class ReviewBaseSchema(BaseModel):
    rating: Optional[int] = Field(None, ge=0, le=10)
    comment: Optional[str] = None

    class Config:
        orm_mode = True


class ReviewCreateSchema(ReviewBaseSchema):
    film_id: int
    rating: int = Field(None, ge=0, le=10)


class ReviewFullCreateSchema(ReviewCreateSchema):
    user_id: int


class ReviewUpdateSchema(ReviewBaseSchema):
    pass


class ReviewSchema(ReviewBaseSchema):
    id: int
    film_id: int
    user_id: int

    class Config:
        orm_mode = True


class ReviewListSchema(BaseModel):
    __root__: List[ReviewSchema]
