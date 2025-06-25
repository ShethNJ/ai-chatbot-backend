import redis.asyncio as redis
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
r = redis.from_url(REDIS_URL, decode_responses=True)

async def get_history(session_id):
    data = await r.lrange(session_id, 0, -1)
    return [eval(x) for x in data]
async def add_message(session_id, msg_dict):
    await r.rpush(session_id, repr(msg_dict))

async def clear_session(session_id):
    await r.delete(session_id)
