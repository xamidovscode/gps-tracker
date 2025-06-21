from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    name: str

class UserOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    name: Optional[str] = None




