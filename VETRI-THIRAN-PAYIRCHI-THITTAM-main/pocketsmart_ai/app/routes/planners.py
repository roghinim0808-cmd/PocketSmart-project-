import json
import os
import uuid
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from ..config import BASE_DIR, settings
from ..database import get_connection
from ..models.schemas import HomeRequest, PartyRequest
from ..security import get_user_id_from_request
from ..services.recommendation_service import make_recommendation

router = APIRouter(tags=["planners"])


def _require_user(request: Request) -> int:
    uid = get_user_id_from_request(request)
    if not uid:
        raise HTTPException(401, "Login required. Please sign in first.")
    return uid


def _save_history(uid: int, planner_type: str, budget: float, request_payload: dict, result: dict):
    conn = get_connection()
    cur = conn.execute("INSERT INTO recommendations(user_id,planner_type,budget,request_json,response_json) VALUES(?,?,?,?,?)", (uid, planner_type, budget, json.dumps(request_payload), json.dumps(result)))
    conn.commit()
    conn.close()
    return cur.lastrowid

@router.post("/api/generate-home")
@router.post("/generate-home", include_in_schema=False)
def generate_home(payload: HomeRequest, request: Request):
    uid = _require_user(request)
    data = payload.model_dump()
    result, ai_used = make_recommendation("home", data)
    result["planner_type"] = "home"; result["budget"] = data["budget"]; result["ai_used"] = ai_used
    rid = _save_history(uid, "home", data["budget"], data, result); result["recommendation_id"] = rid
    return result

@router.post("/api/generate-party")
@router.post("/generate-party", include_in_schema=False)
def generate_party(payload: PartyRequest, request: Request):
    uid = _require_user(request)
    data = payload.model_dump()
    result, ai_used = make_recommendation("party", data)
    result["planner_type"] = "party"; result["budget"] = data["budget"]; result["ai_used"] = ai_used
    rid = _save_history(uid, "party", data["budget"], data, result); result["recommendation_id"] = rid
    return result

@router.post("/api/generate-jewelry")
@router.post("/generate-jewelry", include_in_schema=False)
async def generate_jewelry(
    request: Request,
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("Elegant"),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(None),
):
    uid = _require_user(request)
    if budget <= 0:
        raise HTTPException(422, "Budget must be greater than zero.")
    if len(occasion.strip()) < 2:
        raise HTTPException(422, "Please provide an occasion.")
    image_path = None
    if outfit_image and outfit_image.filename:
        allowed = {"image/jpeg", "image/png", "image/webp"}
        if outfit_image.content_type not in allowed:
            raise HTTPException(400, "Please upload a JPG, PNG, or WEBP image.")
        content = await outfit_image.read()
        if len(content) > settings.max_upload_mb * 1024 * 1024:
            raise HTTPException(400, f"Image must be smaller than {settings.max_upload_mb} MB.")
        upload_dir = BASE_DIR / settings.upload_dir
        upload_dir.mkdir(parents=True, exist_ok=True)
        safe_name = f"{uuid.uuid4().hex}{Path(outfit_image.filename).suffix.lower()}"
        image_path = str(upload_dir / safe_name)
        with open(image_path, "wb") as f:
            f.write(content)
    data = {"budget": budget, "occasion": occasion.strip(), "style": style.strip(), "notes": notes.strip()}
    result, ai_used = make_recommendation("jewelry", data, image_path)
    result["planner_type"] = "jewelry"; result["budget"] = budget; result["ai_used"] = ai_used
    rid = _save_history(uid, "jewelry", budget, data, result); result["recommendation_id"] = rid
    return result

@router.get("/api/recommendations-details/{recommendation_id}")
@router.get("/recommendations-details/{recommendation_id}", include_in_schema=False)
def recommendation_details(recommendation_id: int, request: Request):
    uid = _require_user(request)
    conn = get_connection()
    row = conn.execute("SELECT * FROM recommendations WHERE id=? AND user_id=?", (recommendation_id, uid)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Recommendation not found.")
    result = json.loads(row["response_json"])
    result["recommendation_id"] = row["id"]
    return result

@router.get("/api/history")
@router.get("/history", include_in_schema=False)
def history(request: Request):
    uid = _require_user(request)
    conn = get_connection()
    rows = conn.execute("SELECT id,planner_type,budget,created_at,response_json FROM recommendations WHERE user_id=? ORDER BY id DESC", (uid,)).fetchall()
    conn.close()
    output = []
    for row in rows:
        data = json.loads(row["response_json"])
        output.append({"id": row["id"], "planner_type": row["planner_type"], "budget": row["budget"], "created_at": row["created_at"], "summary": data.get("summary", "")})
    return output
