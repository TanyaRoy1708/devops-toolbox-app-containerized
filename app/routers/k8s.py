from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session

from services.k8s_service import explain_k8s_manifest
from internal import get_db, log_usage

router = APIRouter(prefix="/tools", tags=["k8s"])
templates = Jinja2Templates(directory=str(Path(__file__).parent.parent / "templates"))

@router.get("/k8s", response_class=HTMLResponse)
async def get_k8s(request: Request):
    return templates.TemplateResponse(request, "k8s.html", {"request": request})

@router.post("/k8s", response_class=HTMLResponse)
async def post_k8s(request: Request, manifest: str = Form(...), db: Session = Depends(get_db)):
    # Log usage
    log_usage(db, "k8s")

    result = explain_k8s_manifest(manifest)
    return templates.TemplateResponse(request, "k8s.html", {"request": request, "result": result, "manifest": manifest})
