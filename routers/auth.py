from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from db import get_db

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")


@router.post("/register")
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
        cursor.execute(
            "INSERT INTO users (login, password, fullname, phone, email) VALUES (?, ?, ?, ?, ?)",
            (login, password, fullname, phone, email)
        )
        db.commit()
        return RedirectResponse(url="/login", status_code=303)
    except sqlite3.IntegrityError:
        return templates.TemplateResponse(
            request, "register.html", {"error": "Логин уже занят"}
        )


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.post("/login")
async def login_user(
    request: Request,
    login: str = Form(...),
    password: str = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    user = cursor.execute(
        "SELECT * FROM users WHERE login = ? AND password = ?",
        (login, password)
    ).fetchone()

    if user:
        request.session["user_id"] = user["id"]
        request.session["login"] = user["login"]
        if login == "Conf2027" and password == "Demo77":
            request.session["is_admin"] = True
        return RedirectResponse(url="/requests", status_code=303)
    else:
        return templates.TemplateResponse(
            request, "login.html", {"error": "Неверный логин или пароль"}
        )


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)