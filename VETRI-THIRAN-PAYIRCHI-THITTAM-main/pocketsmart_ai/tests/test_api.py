import os
os.environ["DATABASE_URL"] = "sqlite:///./data/test_pocketsmart.db"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["GEMINI_API_KEY"] = ""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def setup_function():
    # The app creates tables during lifespan. TestClient context is used per test where needed.
    pass

def test_health():
    with TestClient(app) as c:
        r = c.get('/health')
        assert r.status_code == 200
        assert r.json()['status'] == 'ok'

def test_register_and_login():
    with TestClient(app) as c:
        email = 'test@example.com'
        r = c.post('/api/auth/register', json={'name':'Test User','email':email,'password':'secret123'})
        assert r.status_code in (200, 409)
        r = c.post('/api/auth/login', json={'email':email,'password':'secret123'})
        assert r.status_code == 200
        assert c.get('/api/session-info').json()['logged_in'] is True

def test_home_planner():
    with TestClient(app) as c:
        c.post('/api/auth/register', json={'name':'Planner User','email':'planner@example.com','password':'secret123'})
        r = c.post('/api/generate-home', json={'budget':50000,'rooms':['Living Room'],'style':'Modern','notes':''})
        assert r.status_code == 200
        data = r.json()
        assert data['planner_type'] == 'home'
        assert data['recommendation_id'] is not None
