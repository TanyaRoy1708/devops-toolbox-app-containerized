from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import func

from routers import cron, jwt, cidr, k8s, dockerfile_router
from internal import models, engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="DevOps Toolbox")

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Templates
templates_dir = Path(__file__).parent / "templates"
templates_dir.mkdir(parents=True, exist_ok=True)
templates = Jinja2Templates(directory=str(templates_dir))

# Include routers
app.include_router(cron.router)
app.include_router(jwt.router)
app.include_router(cidr.router)
app.include_router(k8s.router)
app.include_router(dockerfile_router.router)

@app.get("/health")
async def health():
    """Liveness probe — used by ALB target group and Docker HEALTHCHECK."""
    return {"status": "ok", "service": "devops-toolbox", "version": "1.0.0"}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    # Get usage counts from DB
    usage_counts = db.query(
        models.ToolUsageLog.tool_name, 
        func.count(models.ToolUsageLog.id)
    ).group_by(models.ToolUsageLog.tool_name).all()
    
    stats = {
        "cron": 0,
        "jwt": 0,
        "cidr": 0,
        "k8s": 0,
        "dockerfile": 0
    }
    
    for tool, count in usage_counts:
        if tool in stats:
            stats[tool] = count
    
    return templates.TemplateResponse(request, "index.html", {
        "request": request, 
        "stats": stats
    })
