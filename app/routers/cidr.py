from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from services.cidr_service import calculate_cidr
from internal import get_db, log_usage, get_cache, set_cache

router = APIRouter(prefix="/tools", tags=["cidr"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/cidr", response_class=HTMLResponse)
async def get_cidr(request: Request):
    return templates.TemplateResponse(request, "cidr.html", {"request": request})

@router.post("/cidr", response_class=HTMLResponse)
async def post_cidr(request: Request, cidr: str = Form(...), db: Session = Depends(get_db)):
    # Log usage
    log_usage(db, "cidr")

    # Check cache
    cache_key = f"cidr:{cidr}"
    cached_result = get_cache(cache_key)
    if cached_result:
        return templates.TemplateResponse(request, "cidr.html", {"request": request, "result": cached_result, "cidr": cidr, "cache_hit": True})

    # Process Request
    result = calculate_cidr(cidr)

    # Set cache (TTL 1 hour)
    set_cache(cache_key, result, ttl=3600)

    return templates.TemplateResponse(request, "cidr.html", {"request": request, "result": result, "cidr": cidr, "cache_hit": False})


