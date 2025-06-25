import logging, os, time
from contextlib import contextmanager

os.makedirs("logs", exist_ok=True)

# Create custom logger
logger = logging.getLogger("chatbot")
logger.setLevel(logging.INFO)

# File handler with formatter
handler = logging.FileHandler("logs/chatbot.log")
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(user_id)s | %(message_text)s | RESP:%(response)s| Escalated: %(escalated)s | Latency: %(latency)s'
)

handler.setFormatter(formatter)
logger.addHandler(handler)

# Logging functions
def log_interaction(user_id, message, response, escalated, latency=None):
    logger.info("User interaction logged", extra={
        "user_id": user_id or "-",
        "message_text": message or "-",
        "response": response or "-",
        "escalated": escalated,
        "latency": f"{latency:.2f}ms" if latency is not None else "-"
    })

def log_connection(user_id):
    logger.info("User connected", extra={
        "user_id": user_id,
        "message_text": "-",
        "response": "-",
        "escalated": False,
        "latency": "-"
    })

def log_disconnection(user_id):
    logger.info("User disconnected", extra={
        "user_id": user_id,
        "message_text": "-",
        "response": "-",
        "escalated": False,
        "latency": "-"
    })

def log_error(user_id, message, error):
    logger.error(f"Error occurred: {str(error)}", extra={
        "user_id": user_id,
        "message_text": message,
        "response": str(error),
        "escalated": False,
        "latency": "-"
    })

import time
from contextlib import contextmanager
from utils.logger import log_error, log_interaction

@contextmanager
def gpt_latency_timer(user_id, message=""):
    start = time.perf_counter()
    log_data = {
        "response": "-",
        "escalated": False
    }

    try:
        yield log_data 
    except Exception as e:
        log_data["escalated"] = True
        log_data["response"] = str(e)
        log_error(user_id, message, e)
        raise
    finally:
        latency = (time.perf_counter() - start) * 1000
        log_interaction(
            user_id=user_id,
            message=message,
            response=log_data["response"],
            escalated=log_data["escalated"],
            latency=latency
        )
