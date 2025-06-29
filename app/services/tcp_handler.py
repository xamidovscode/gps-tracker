import asyncio
import redis.asyncio as redis
import json


REDIS_URL = "redis://localhost:6379/0"
CHANNEL = "fmb920_data"


def create_redis_pool():
    return redis.ConnectionPool.from_url(REDIS_URL, decode_responses=True)


redis_pool = create_redis_pool()
REDIS = redis.Redis(connection_pool=redis_pool)


async def handle_client(reader, writer):
    addr = writer.get_extra_info("peername")
    imei = None

    try:
        while True:
            data: bytes = await reader.read(1024)
            if not data:
                break

            decoded_data = data.decode("utf-8", errors="ignore")

            if len(decoded_data) == 17 and decoded_data.startswith('\x00\x0f'):
                imei = decoded_data.lstrip("\x00\x0f")
                writer.write(b'\x01')
                await writer.drain()
                continue

            json_data = decoded_data
            print(json_data)
            await REDIS.publish(CHANNEL, json.dumps({'imei': imei, 'data': json_data}))

    except Exception as e:
        print(f"❌ [{addr}] Xatolik: {e}")

    finally:
        writer.close()
        await writer.wait_closed()


async def start():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 5000)

    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(start())
