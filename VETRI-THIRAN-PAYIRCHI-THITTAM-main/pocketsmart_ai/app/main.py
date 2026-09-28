from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import BASE_DIR, settings
from .database import init_db
from .routes.auth import router as auth_router
from .routes.pages import router as pages_router
from .routes.planners import router as planner_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    (BASE_DIR / settings.upload_dir).mkdir(parents=True, exist_ok=True)
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
    description="Budget-aware AI recommendation assistant",
)
app.add_middleware(CORSMiddleware, allow_origins=["http://127.0.0.1:8000", "http://localhost:8000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "app" / "static")), name="static")
app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(planner_router)

@app.get("/health")
def health():
    return {"status": "ok", "ai_configured": bool(settings.gemini_api_key), "model": settings.gemini_model}

@app.get("/startup")
def startup_status():
    return health()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
