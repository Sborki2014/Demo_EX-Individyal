from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3

from db import get_db

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, db: sqlite3.Connection = Depends(get_db)):
    if not request.session.get("is_admin"):
        return RedirectResponse(url="/login", status_code=303)

    cursor = db.cursor()
    all_requests = cursor.execute("SELECT * FROM requests").fetchall()

    return templates.TemplateResponse(
        request, "admin.html", {"requests": all_requests}
    )


@router.post("/admin/update_status/{req_id}")
async def update_status(
    req_id: int,
    status: str = Form(...),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    cursor.execute(
        "UPDATE requests SET status = ? WHERE id = ?",
        (status, req_id)
    )
    db.commit()
    return RedirectResponse(url="/admin", status_code=303)