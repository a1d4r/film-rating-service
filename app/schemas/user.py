from typing import List, Optional

from pydantic import BaseModel, SecretStr


class UserBaseSchema(BaseModel):
    login: Optional[str]

    class Config:
        orm_mode = True


class UserCreateSchema(UserBaseSchema):
    login: str
    password: SecretStr


class UserUpdateSchema(UserBaseSchema):
    password: Optional[SecretStr]


class UserSchema(UserBaseSchema):
    login: str
    id: int


class UserListSchema(BaseModel):
    __root__: List[UserSchema]
