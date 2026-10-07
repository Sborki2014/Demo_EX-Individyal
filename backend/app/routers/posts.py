from fastapi import APIRouter, HTTPException, Path, Query, Body
from typing import List, Dict, Optional
from typing_extensions import Annotated 
from app.schemas import Post, PostCreate
from app.database import posts, users

router = APIRouter(
    prefix="/items", # Оставляем ваш префикс /items
    tags=["Публикации (Посты)"]
)

@router.get('/', response_model=List[Post])
async def get_all_posts():
    return posts

@router.post('/add', response_model=Post)
async def add_item(post: Annotated[
    PostCreate,
    Body(..., example={
        'title': 'TitleName',
        'body': 'BodyName',
        'author_id': 1  # Исправили пример, теперь он валидный
    })
]):
    author = next((user for user in users if user['id'] == post.author_id), None)
    if not author:
        raise HTTPException(status_code=404, detail='User not found')

    new_post_id = max([p['id'] for p in posts], default=0) + 1
    new_post = {'id': new_post_id, 'title': post.title, 'body': post.body, 'author': author}
    posts.append(new_post)
    return new_post

@router.get('/search', response_model=Dict[str, Optional[Post]])  
async def search_post(post_id: Annotated[
    Optional[int],
    Query(title='ID of post to search for', ge=1, le=50)
] = None):
    if post_id:
        for post in posts:
            if post['id'] == post_id:
               return {'data': post}
        raise HTTPException(status_code=404, detail='Post not found')
    return {'data': None}

@router.get('/{id}', response_model=Post)
async def get_post_by_id(id: Annotated[int, Path(..., title='Здесь указывается id поста', ge=1)]):
    for post in posts:
        if post['id'] == id:
            return post
     
    raise HTTPException(status_code=404, detail='Post not found')
