import json
import redis.asyncio as redis
from bot.core.config import REDIS_URL

redis_client = redis.from_url(REDIS_URL, decode_responses=True)

async def add_to_queue(chat_id: int, track_data: dict):
    await redis_client.rpush(f"queue:{chat_id}", json.dumps(track_data))

async def get_queue(chat_id: int) -> list:
    data = await redis_client.lrange(f"queue:{chat_id}", 0, -1)
    return [json.loads(x) for x in data]

async def pop_queue(chat_id: int) -> dict:
    data = await redis_client.lpop(f"queue:{chat_id}")
    return json.loads(data) if data else None

async def clear_queue(chat_id: int):
    await redis_client.delete(f"queue:{chat_id}")

async def remove_specific_track(chat_id: int, index: int) -> bool:
    queue = await get_queue(chat_id)
    if 0 <= index < len(queue):
        queue.pop(index)
        await clear_queue(chat_id)
        if queue:
            await redis_client.rpush(f"queue:{chat_id}", *[json.dumps(x) for x in queue])
        return True
    return False