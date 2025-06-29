from sqlalchemy import Column, Integer, String, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GpsData(Base):
    __tablename__ = "gps_data"

    id = Column(Integer, primary_key=True, index=True)
    imei = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    class Config:
        orm_mode = True