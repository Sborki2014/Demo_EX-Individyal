from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import sqlite3
from db import init_db

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

# Подключаем шаблоны и статику
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Инициализация БД при старте
init_db()

def get_db():
    conn = sqlite3.connect('conferences.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- ГЛАВНАЯ (Перенаправление) ---
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if "user_id" in request.session:
        return RedirectResponse(url="/requests", status_code=303)
    return RedirectResponse(url="/login", status_code=303)

# --- РЕГИСТРАЦИЯ (Модуль 1.2) ---
@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")

@app.post("/register")
async def register_user(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    fullname: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO users (login, password, fullname, phone, email) VALUES (?, ?, ?, ?, ?)",
                       (login, password, fullname, phone, email))
        db.commit()
        return RedirectResponse(url="/login", status_code=303)
    except sqlite3.IntegrityError:
        return templates.TemplateResponse(request, "register.html", {"error": "Логин уже занят"})

# --- АВТОРИЗАЦИЯ (Модуль 1.2) ---
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.post("/login")
async def login_user(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    user = cursor.execute("SELECT * FROM users WHERE login = ? AND password = ?", (login, password)).fetchone()
    
    if user:
        request.session["user_id"] = user["id"]
        request.session["login"] = user["login"]
        # Проверка на админа
        if login == "Conf2027" and password == "Demo77":
            request.session["is_admin"] = True
        return RedirectResponse(url="/requests", status_code=303)
    else:
        return templates.TemplateResponse(request, "login.html", {"error": "Неверный логин или пароль"})

# --- СОЗДАНИЕ ЗАЯВКИ (Модуль 1.3) ---
@app.get("/create_request", response_class=HTMLResponse)
async def create_request_page(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request, "create_request.html")

@app.post("/create_request")
async def create_request(
    request: Request,
    room: str = Form(...),
    date: str = Form(...),
    payment: str = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
        
    cursor = db.cursor()
    cursor.execute("INSERT INTO requests (user_id, room_name, start_date, payment_method) VALUES (?, ?, ?, ?)",
                   (request.session["user_id"], room, date, payment))
    db.commit()
    return RedirectResponse(url="/requests", status_code=303)

# --- ПРОСМОТР ЗАЯВОК (Модуль 1.3) ---
@app.get("/requests", response_class=HTMLResponse)
async def view_requests(request: Request, db: sqlite3.Connection = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    
    cursor = db.cursor()
    user_requests = cursor.execute("SELECT * FROM requests WHERE user_id = ?", (request.session["user_id"],)).fetchall()
    return templates.TemplateResponse(request, "requests.html", {"requests": user_requests})

# --- ОТЗЫВ (Модуль 1.3, 3.7) ---
@app.post("/add_review/{req_id}")
async def add_review(req_id: int, request: Request, review: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    
    cursor = db.cursor()
    # Отзыв можно оставить только если статус "Завершено"
    cursor.execute("UPDATE requests SET review = ? WHERE id = ? AND status = 'Завершено'", (review, req_id))
    db.commit()
    return RedirectResponse(url="/requests", status_code=303)

# --- Админ-Панель (Модуль 1.4) ---
@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, db: sqlite3.Connection = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login", status_code=303)
    
    cursor = db.cursor()
    all_requests = cursor.execute("SELECT * FROM requests").fetchall()
    return templates.TemplateResponse(request, "admin.html", {"requests": all_requests})

@app.post("/admin/update_status/{req_id}")
async def update_status(req_id: int, status: str = Form(...), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("UPDATE requests SET status = ? WHERE id = ?", (status, req_id))
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)

# --- ВЫХОД ---
@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)


@app.get("/orders")
async def get_orders(status: str = None, user_id: int = None):
    pass