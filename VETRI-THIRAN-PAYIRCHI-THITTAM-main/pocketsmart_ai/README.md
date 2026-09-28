# PocketSmart AI

PocketSmart AI is a complete FastAPI + Jinja2 web application based on the supplied project document. It provides:

- Home Interior Budget Planner
- Party Budget Planner
- Jewelry Budget Planner with optional outfit image upload
- Gemini multimodal AI integration
- Safe deterministic fallback recommendations when no Gemini key is configured or the AI request fails
- User registration/login/logout with JWT sessions
- Recommendation history and dashboard
- Budget allocation and platform-link generation
- Responsive HTML/CSS/JavaScript frontend
- SQLite database for local development
- Automated API tests

## Important implementation note

The supplied document mentions Gemini 1.5 Flash Pro and several third-party platforms. Those model/platform APIs are not supplied with credentials, so this implementation uses the current Google GenAI SDK and a configurable Gemini model. The default model is `gemini-3.8-flash`; change `GEMINI_MODEL` in `.env` if your account uses another supported model.

The product/vendor links are generated as search links and the catalog is intentionally mock/curated. This keeps the project runnable without private Amazon, Flipkart, IKEA, Swiggy, Zomato, or OYO API credentials.

## 1. VS Code setup

1. Install Python 3.11+.
2. Open this folder in VS Code.
3. Open Terminal -> New Terminal.
4. Create a virtual environment:

### Windows PowerShell
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Windows CMD
```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
```

5. Install dependencies:
```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env`.

### Windows PowerShell
```powershell
Copy-Item .env.example .env
```

7. For AI mode, put your Gemini API key in `.env`:
```env
GEMINI_API_KEY=your_key_here
```

If you leave it blank, the application still runs using the built-in fallback recommendation engine.

## 2. Run the application

```bash
uvicorn app.main:app --reload
```

Open:

`http://127.0.0.1:8000`

API documentation:

`http://127.0.0.1:8000/docs`

## 3. Test

In another terminal:
```bash
pytest -q
```

## 4. Main routes

### Pages
- `/` Home
- `/register` Register
- `/login` Login
- `/dashboard` Dashboard
- `/planner/home` Home planner
- `/planner/party` Party planner
- `/planner/jewelry` Jewelry planner
- `/history` Recommendation history

### API
- `POST /api/auth/register`
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/session-info`
- `GET /api/session-data`
- `POST /api/generate-home`
- `POST /api/generate-party`
- `POST /api/generate-jewelry`
- `GET /api/recommendations-details/{recommendation_id}`
- `GET /api/history`
- `GET /health`

The legacy-style paths from the supplied document are also available as aliases:
- `/generate-home`
- `/generate-party`
- `/generate-jewelry`
- `/session-info`
- `/session-data`
- `/history`
- `/recommendations-details/{recommendation_id}`

## 5. Project structure

```text
pocketsmart_ai/
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── security.py
│   ├── models/
│   │   ├── db_models.py
│   │   └── schemas.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── pages.py
│   │   └── planners.py
│   ├── services/
│   │   ├── gemini_utils.py
│   │   ├── recommendation_service.py
│   │   └── catalog_service.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   ├── history.html
│   │   ├── planner_home.html
│   │   ├── planner_party.html
│   │   └── planner_jewelry.html
│   └── static/
│       ├── css/style.css
│       └── js/app.js
├── data/
├── uploads/
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```
