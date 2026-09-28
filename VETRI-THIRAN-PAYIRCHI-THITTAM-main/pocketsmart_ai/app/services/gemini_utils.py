import json
from pathlib import Path
from typing import Any
from google import genai
from google.genai import types
from PIL import Image
from ..config import settings


def _client():
    if not settings.gemini_api_key:
        return None
    return genai.Client(api_key=settings.gemini_api_key)


def _prompt(planner_type: str, payload: dict[str, Any], catalog: list[dict[str, Any]]) -> str:
    return f"""
You are PocketSmart AI, a practical budget recommendation assistant.
Planner: {planner_type}
User input JSON: {json.dumps(payload, ensure_ascii=False)}
Candidate catalog: {json.dumps(catalog, ensure_ascii=False)}

Return ONLY valid JSON with this exact shape:
{{
  "summary": "short practical summary",
  "allocation": {{"category": number}},
  "recommendations": [
    {{"name":"...","category":"...","price":number,"platform":"...","url":"...","reason":"..."}}
  ],
  "tips": ["...", "..."]
}}
Rules:
- Never exceed the user's total budget when the recommendation prices are summed.
- Prefer the provided candidate catalog and keep its URLs unchanged.
- Do not invent a live price or claim that a product is currently in stock.
- If candidates are insufficient, choose a smaller set and explain it in tips.
- Keep recommendations useful for a student project demo.
""".strip()


def generate_recommendation(planner_type: str, payload: dict[str, Any], catalog: list[dict[str, Any]], image_path: str | None = None) -> tuple[dict[str, Any] | None, bool]:
    client = _client()
    if client is None:
        return None, False
    try:
        contents: list[Any] = [_prompt(planner_type, payload, catalog)]
        if image_path:
            image = Image.open(image_path)
            contents.append(image)
            contents[0] += "\nAn outfit image is attached. Use it only for broad color/style coordination. Do not identify the person."
        response = client.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=types.GenerateContentConfig(
                temperature=0.3,
                max_output_tokens=1800,
                response_mime_type="application/json",
            ),
        )
        text = (response.text or "").strip()
        if not text:
            return None, False
        data = json.loads(text)
        return data, True
    except Exception:
        return None, False
