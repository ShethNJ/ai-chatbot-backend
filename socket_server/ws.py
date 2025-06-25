import socketio
import time
from services.chat import process_message
from utils.redis_client import clear_session
from utils.logger import log_interaction, log_error

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
sio_app = socketio.ASGIApp(sio)

@sio.event
async def connect(sid, environ):
    print(f"[CONNECT] {sid}")

@sio.event
async def message(sid, data):
    try:
        session_id = data.get("session_id")
        user_id = data.get("user_id")
        user_msg = data.get("message")

        if not session_id or not user_id or not user_msg:
            await sio.emit("bot_response", {
                "session_id": session_id or "unknown",
                "message": "⚠️ Invalid input. Please check your message format.",
                "escalated": False
            }, to=sid)
            log_error(user_id or "unknown", user_msg or "", "Invalid message payload received")
            return

        # ✅ Start measuring latency
        start_time = time.perf_counter()

        # 🔄 Main logic
        bot_resp, escalated = await process_message(session_id, user_id, user_msg)

        # ✅ End measuring latency
        latency_ms = (time.perf_counter() - start_time) * 1000  # milliseconds

        # 🔁 Send response back to user
        await sio.emit("bot_response", {
            "session_id": session_id,
            "message": bot_resp,
            "escalated": escalated
        }, to=sid)

        # ✅ Log interaction with latency
        log_interaction(user_id, user_msg, bot_resp, escalated, latency=latency_ms)

    except Exception as e:
        print(f"[ERROR] while handling message from {sid}: {e}")
        await sio.emit("bot_response", {
            "session_id": data.get("session_id", "unknown"),
            "message": "⚠️ An error occurred while processing your request.",
            "escalated": False
        }, to=sid)
        log_error(data.get("user_id", "unknown"), data.get("message", ""), str(e))

@sio.event
async def disconnect(sid):
    print(f"[DISCONNECT] {sid}")
    await clear_session(sid)
