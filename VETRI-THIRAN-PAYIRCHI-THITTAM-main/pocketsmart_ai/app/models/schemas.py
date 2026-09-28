from typing import Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: list[str] = Field(min_length=1)
    style: str = Field(default="Modern", max_length=80)
    notes: str = Field(default="", max_length=1000)

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guest_count: int = Field(gt=0, le=10_000)
    event_type: str = Field(min_length=2, max_length=80)
    venue: str = Field(default="Flexible", max_length=120)
    notes: str = Field(default="", max_length=1000)

class RecommendationItem(BaseModel):
    name: str
    category: str
    price: float
    platform: str
    url: str
    reason: str

class RecommendationResponse(BaseModel):
    model_config = ConfigDict(extra="allow")
    planner_type: str
    budget: float
    allocation: dict[str, float]
    summary: str
    recommendations: list[RecommendationItem]
    tips: list[str] = []
    ai_used: bool = False
    recommendation_id: int | None = None

class HistoryItem(BaseModel):
    id: int
    planner_type: str
    budget: float
    created_at: str
    summary: str
