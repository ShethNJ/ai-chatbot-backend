import os
import httpx
from dotenv import load_dotenv
from utils.logger import gpt_latency_timer, log_error

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"
DEFAULT_MODEL = "openai/gpt-3.5-turbo-16k"

async def ask_gpt(messages, user_id="anonymous"):
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages
    }

    print(f"[DEBUG] API_KEY loaded: {'Yes' if API_KEY else 'No'}")
    print(f"[DEBUG] Sending payload: {payload}")

    try:
        with gpt_latency_timer(user_id, messages[-1]["content"]):
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post(API_URL, headers=headers, json=payload)
                print(f"[DEBUG] Response status code: {resp.status_code}")
                print(f"[DEBUG] Response body: {resp.text}")

                resp.raise_for_status()

                data = resp.json()
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    log_error(user_id, messages[-1]["content"], "No choices in response")
                    return "⚠️ Sorry, I couldn't get a proper response."
    except Exception as e:
        log_error(user_id, messages[-1]["content"], str(e))
        print(f"[DEBUG] Exception during API call: {e}")
        return "⚠️ Sorry, I'm having trouble responding right now. Please try again later."
