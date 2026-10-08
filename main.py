from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from db import init_db
from routers import auth, requests, admin


# Создаём приложение
app = FastAPI()

# Сессии (нужны для логина)
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Статика (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация БД
init_db()

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(requests.router)
app.include_router(admin.router)


@app.get("/")
async def index(request: Request):
    if "user_id" in request.session:
        return RedirectResponse(url="/requests", status_code=303)
    return RedirectResponse(url="/login", status_code=303)