from typing import Optional, Annotated
from pydantic import BaseModel, Field

class User(BaseModel):
    id: int
    name: str
    age: int

class Post(BaseModel):
    id: int
    title: str
    body: str
    author: User

class PostCreate(BaseModel):
    title: Annotated[
        str, Field(..., title='Заголовок поста', min_length=2, max_length=35)
    ]
    body: Annotated[
        str, Field(..., title='Описание поста')
    ]
    author_id: Annotated[
        int, Field(..., title='ID автора', ge=1)
    ]

class UserCreate(BaseModel):
    name: Annotated[
        str, Field(..., title='Имя пользователя', min_length=2, max_length=20)
    ]
    age: Annotated[
        int, Field(..., title='Возраст пользователя', ge=1, le=120)
    ]
