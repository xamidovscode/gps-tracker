from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import async_session
from app.models.gps import GpsData
from app.schemas.gps import GpsDataOut
from typing import List

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.get("/gps", response_model=List[GpsDataOut])
async def get_gps_data(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GpsData).order_by(GpsData.created_at.desc()).limit(50))
    return result.scalars().all()

