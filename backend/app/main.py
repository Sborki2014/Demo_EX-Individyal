from fastapi import FastAPI
from app.routers import users, posts

app = FastAPI(
    title="Моё первое разделенное приложение",
    version="1.0.0"
)

# Подключаем изолированные модули
app.include_router(users.router)
app.include_router(posts.router)

@app.get('/')
async def root():
    return {"message": "Приложение работает. Перейдите на /docs"}
