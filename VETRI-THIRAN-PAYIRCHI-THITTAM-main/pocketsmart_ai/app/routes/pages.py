from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import get_connection
from ..security import get_user_id_from_request
from ..config import BASE_DIR

router = APIRouter(tags=["pages"])
templates = Jinja2Templates(directory=str(BASE_DIR / "app" / "templates"))

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.get("/dashboard")
def dashboard(request: Request):
    if not get_user_id_from_request(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/history")
def history_page(request: Request):
    if not get_user_id_from_request(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("history.html", {"request": request})

@router.get("/planner/home")
def home_planner(request: Request):
    if not get_user_id_from_request(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("planner_home.html", {"request": request})

@router.get("/planner/party")
def party_planner(request: Request):
    if not get_user_id_from_request(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("planner_party.html", {"request": request})

@router.get("/planner/jewelry")
def jewelry_planner(request: Request):
    if not get_user_id_from_request(request):
        return RedirectResponse("/login", status_code=303)
    return templates.TemplateResponse("planner_jewelry.html", {"request": request})
