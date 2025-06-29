from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal, engine
import schemas
import models
import db

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/admin/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/trackers", response_model=list[schemas.GpsDataOut])
def get_user(db: Session = Depends(db.get_db)):
    users = db.query(models.GpsData).all()
    return users
