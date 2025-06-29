from pydantic import BaseModel
from datetime import datetime

class GpsDataOut(BaseModel):
    id: int
    imei: str
    lat: float
    lon: float
    created_at: datetime

    class Config:
        orm_mode = True

