from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from db import get_db
from security import hash_password, verify_password

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
        hashed = hash_password(password)
        cursor.execute(
            "INSERT INTO users (login, password, fullname, phone, email) VALUES (?, ?, ?, ?, ?)",
            (login, hashed, fullname, phone, email)
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
        "SELECT * FROM users WHERE login = ?",
        (login,)
    ).fetchone()

    if user and verify_password(password, user["password"]):
        request.session["user_id"] = user["id"]
        request.session["login"] = user["login"]
        if login == "Conf2027":
            request.session["is_admin"] = True
        return RedirectResponse(url="/requests", status_code=303)

    return templates.TemplateResponse(
        request, "login.html", {"error": "Неверный логин или пароль"}
    )


@router.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)