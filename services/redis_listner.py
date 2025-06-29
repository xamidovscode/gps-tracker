import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
import json
import redis.asyncio as redis

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.models.gps import GpsData
from app.core.config import settings

redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True)
DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def save_to_db(data: dict):
    async with async_session() as session:
        imei = data.get("imei")
        payload = data.get("data")

        if isinstance(payload, str):
            try:
                payload = json.loads(payload)
            except Exception as e:
                print("Invalid payload JSON:", e)
                return

        latlng_str = payload.get("state", {}).get("reported", {}).get("latlng")
        if not latlng_str:
            print("latlng not found.")
            return

        try:
            lat_str, lon_str = latlng_str.split(",")
            lat = float(lat_str)
            lon = float(lon_str)
        except Exception as e:
            print("latlng parsing error:", e)
            return

        gps = GpsData(imei=imei, lat=lat, lon=lon)
        session.add(gps)
        await session.commit()
        print("Data saved:", gps.imei, gps.lat, gps.lon)

async def listen_to_redis():
    pubsub = redis_client.pubsub()
    await pubsub.subscribe(settings.CHANNEL)
    print(f"Listening to Redis channel: {settings.CHANNEL}")

    async for message in pubsub.listen():
        if message["type"] == "message":
            try:
                data = json.loads(message["data"])
                await save_to_db(data)
            except Exception as e:
                print("JSON parse/save error:", e)

if __name__ == "__main__":
    asyncio.run(listen_to_redis())
