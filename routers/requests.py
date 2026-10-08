from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/requests", response_class=HTMLResponse)
async def view_requests(request: Request, db: sqlite3.Connection = Depends(get_db)):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    cursor = db.cursor()
    user_requests = cursor.execute(
        "SELECT * FROM requests WHERE user_id = ?",
        (request.session["user_id"],)
    ).fetchall()

    return templates.TemplateResponse(
        request, "requests.html", {"requests": user_requests}
    )


@router.get("/create_request", response_class=HTMLResponse)
async def create_request_page(request: Request):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request, "create_request.html")


@router.post("/create_request")
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
    cursor.execute(
        "INSERT INTO requests (user_id, room_name, start_date, payment_method) VALUES (?, ?, ?, ?)",
        (request.session["user_id"], room, date, payment)
    )
    db.commit()
    return RedirectResponse(url="/requests", status_code=303)


@router.post("/add_review/{req_id}")
async def add_review(
    req_id: int,
    request: Request,
    review: str = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    if "user_id" not in request.session:
        return RedirectResponse(url="/login", status_code=303)

    cursor = db.cursor()
    cursor.execute(
        "UPDATE requests SET review = ? WHERE id = ? AND status = 'Завершено'",
        (review, req_id)
    )
    db.commit()
    return RedirectResponse(url="/requests", status_code=303)