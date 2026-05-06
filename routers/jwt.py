from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from services.jwt_service import decode_jwt
from internal import get_db, log_usage, get_cache, set_cache

router = APIRouter(prefix="/tools", tags=["jwt"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/jwt", response_class=HTMLResponse)
async def get_jwt(request: Request):
    return templates.TemplateResponse(request, "jwt.html", {"request": request})

@router.post("/jwt", response_class=HTMLResponse)
async def post_jwt(request: Request, token: str = Form(...), db: Session = Depends(get_db)):
    # Log usage
    log_usage(db, "jwt")

    # Check cache
    cache_key = f"jwt:{token}"
    cached_result = get_cache(cache_key)
    if cached_result:
        return templates.TemplateResponse(request, "jwt.html", {"request": request, "result": cached_result, "token": token, "cache_hit": True})

    # Process Request
    result = decode_jwt(token)

    # Set cache (TTL 1 hour)
    set_cache(cache_key, result, ttl=3600)

    return templates.TemplateResponse(request, "jwt.html", {"request": request, "result": result, "token": token, "cache_hit": False})
