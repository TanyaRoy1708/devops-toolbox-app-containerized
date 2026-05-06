from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from services.cron_service import explain_cron
from internal import get_db, log_usage, get_cache, set_cache

router = APIRouter(prefix="/tools", tags=["cron"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/cron", response_class=HTMLResponse)
async def get_cron(request: Request):
    return templates.TemplateResponse(request, "cron.html", {"request": request})

@router.post("/cron", response_class=HTMLResponse)
async def post_cron(request: Request, expression: str = Form(...), db: Session = Depends(get_db)):
    # Log usage
    log_usage(db, "cron")

    # Check cache
    cache_key = f"cron:{expression}"
    cached_result = get_cache(cache_key)
    if cached_result:
        return templates.TemplateResponse(request, "cron.html", {"request": request, "result": cached_result, "cache_hit": True})

    # Process Request
    result = explain_cron(expression)

    # Set cache (TTL 1 hour)
    set_cache(cache_key, result, ttl=3600)

    return templates.TemplateResponse(request, "cron.html", {"request": request, "result": result, "cache_hit": False})
