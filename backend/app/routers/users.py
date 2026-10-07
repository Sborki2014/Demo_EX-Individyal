from fastapi import APIRouter, Body
from typing import Optional
from typing_extensions import Annotated  # Annotated импортируем отсюда
from app.schemas import User, UserCreate
from app.database import users

router = APIRouter(
    prefix="/users",
    tags=["Пользователи"]
)

@router.post('/add', response_model=User)
async def user_add(user: Annotated[
    UserCreate,
    Body(..., example={'name': 'UserName', 'age': 18})
]):
    # Безопасная генерация ID: берем максимальный существующий и прибавляем 1
    new_user_id = max([u['id'] for u in users], default=0) + 1
    new_user = {'id': new_user_id, 'name': user.name, 'age': user.age}
    
    users.append(new_user)
    return new_user
