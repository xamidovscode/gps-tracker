# app/main.py
from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="FMB920 GPS API")

app.include_router(router)
