@echo off
if not exist .venv (
  py -3.13 -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
if not exist .env copy .env.example .env
uvicorn app.main:app --reload
