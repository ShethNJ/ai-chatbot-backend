from textblob import TextBlob
import time
from utils.redis_client import get_history, add_message
from utils.gpt import ask_gpt

ESCALATION_KEYWORDS = {"human", "agent", "support", "help me", "talk to"}

def needs_escalation(text: str) -> bool:
    """
    Returns True if text suggests escalation based on keywords or negative sentiment.
    """
    # Keyword check
    lowered = text.lower()
    keyword_triggered = any(keyword in lowered for keyword in ESCALATION_KEYWORDS)

    # Sentiment check
    sentiment_score = TextBlob(text).sentiment.polarity
    sentiment_triggered = sentiment_score < -0.3

    return keyword_triggered or sentiment_triggered

async def process_message(session_id: str, user_id: str, text: str):
    """
    Handles a user message, determines escalation (via keywords + sentiment),
    gets GPT response, and updates history.
    """
    start_time = time.time()
    try:
        escalated = needs_escalation(text)

        history = await get_history(session_id)
        history.append({"role": "user", "content": text})

        response = await ask_gpt(history, user_id=user_id)

        if escalated:
            response += "\n\n I’ll escalate this to a human agent."

        await add_message(session_id, {"role": "assistant", "content": response})

        latency = (time.time() - start_time) * 1000
        return response, escalated

    except Exception as e:
        return "⚠️ Sorry, something went wrong while processing your message.", False
