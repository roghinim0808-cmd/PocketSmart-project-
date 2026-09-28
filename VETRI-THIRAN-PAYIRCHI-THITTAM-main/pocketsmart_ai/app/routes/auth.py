from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from ..database import get_connection
from ..models.schemas import RegisterRequest, LoginRequest
from ..security import hash_password, verify_password, create_access_token, get_user_id_from_request

router = APIRouter(tags=["auth"])

@router.post("/api/auth/register")
@router.post("/register", include_in_schema=False)
def register(payload: RegisterRequest, response: Response):
    conn = get_connection()
    try:
        existing = conn.execute("SELECT id FROM users WHERE lower(email)=lower(?)", (payload.email,)).fetchone()
        if existing:
            raise HTTPException(409, "An account with this email already exists.")
        cur = conn.execute("INSERT INTO users(name,email,password_hash) VALUES(?,?,?)", (payload.name.strip(), payload.email.lower(), hash_password(payload.password)))
        conn.commit()
        token = create_access_token(cur.lastrowid)
        response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=60*120)
        return {"message": "Registration successful", "user_id": cur.lastrowid}
    finally:
        conn.close()

@router.post("/api/auth/login")
@router.post("/login", include_in_schema=False)
def login(payload: LoginRequest, response: Response):
    conn = get_connection()
    try:
        user = conn.execute("SELECT * FROM users WHERE lower(email)=lower(?)", (payload.email,)).fetchone()
        if not user or not verify_password(payload.password, user["password_hash"]):
            raise HTTPException(401, "Invalid email or password.")
        token = create_access_token(user["id"])
        response.set_cookie("access_token", token, httponly=True, samesite="lax", max_age=60*120)
        return {"message": "Login successful", "user": {"id": user["id"], "name": user["name"], "email": user["email"]}}
    finally:
        conn.close()

@router.post("/api/auth/logout")
@router.get("/logout", include_in_schema=False)
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}

@router.get("/api/session-info")
@router.get("/session-info", include_in_schema=False)
def session_info(request: Request):
    uid = get_user_id_from_request(request)
    if not uid:
        return {"logged_in": False, "user": None}
    conn = get_connection()
    user = conn.execute("SELECT id,name,email FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    return {"logged_in": bool(user), "user": dict(user) if user else None}

@router.get("/api/session-data")
@router.get("/session-data", include_in_schema=False)
def session_data(request: Request):
    uid = get_user_id_from_request(request)
    if not uid:
        raise HTTPException(401, "Login required.")
    conn = get_connection()
    count = conn.execute("SELECT COUNT(*) AS c FROM recommendations WHERE user_id=?", (uid,)).fetchone()["c"]
    conn.close()
    return {"user_id": uid, "recommendation_count": count}
