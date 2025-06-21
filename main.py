from fastapi import FastAPI

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal, engine
from models import Base, User
from schemas import UserCreate, UserOut, UserUpdate

from typing import List

Base.metadata.create_all(bind=engine)

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

@app.post("/user/create/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=List[UserOut])
def create_user(db: Session = Depends(get_db)):
    return db.query(User).filter(User.name == 'string')



@app.get("/users/{user_id}", response_model=UserOut)
def create_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=400, detail=f"User not found by {user_id}")

    return user


@app.patch("/users/{user_id}", response_model=UserOut)
def create_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=400, detail=f"User not found by {user_id}")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

